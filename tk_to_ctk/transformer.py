"""LibCST-based source transformer for tkinter to customtkinter conversion."""

from __future__ import annotations

import ast
from collections import defaultdict
from typing import Iterable

import libcst as cst
from libcst import metadata

from .analysis import ImportAnalysis
from .listbox_template import LISTBOX_TEMPLATE
from .mappings import TK_MODULE_NAMES, TK_VARIABLE_NAMES, WIDGET_RULES, get_widget_rule
from .models import ConversionOptions, Diagnostic, DiagnosticLevel, WidgetRule


def _expr(code: str) -> cst.BaseExpression:
    return cst.parse_expression(code)


def _stmt(code: str) -> cst.BaseStatement:
    return cst.parse_statement(f"{code}\n")


class ImportUsageCollector(cst.CSTVisitor):
    """Collect whether the transformed module still references tk/ttk/ctk."""

    def __init__(self) -> None:
        self.uses_tk = False
        self.uses_ttk = False
        self.uses_ctk = False

    def visit_Attribute(self, node: cst.Attribute) -> None:
        if isinstance(node.value, cst.Name):
            if node.value.value == "tk":
                self.uses_tk = True
            elif node.value.value == "ttk":
                self.uses_ttk = True
            elif node.value.value == "ctk":
                self.uses_ctk = True

    def visit_Name(self, node: cst.Name) -> None:
        if node.value == "CTkListbox":
            self.uses_ctk = True


class TkinterToCustomTkinterTransformer(cst.CSTTransformer):
    """Transform tkinter source into safer customtkinter source."""

    METADATA_DEPENDENCIES = (metadata.ParentNodeProvider, metadata.PositionProvider)

    def __init__(self, analysis: ImportAnalysis, options: ConversionOptions) -> None:
        self.analysis = analysis
        self.options = options
        self.diagnostics: list[Diagnostic] = []
        self.comments_by_line: dict[int, list[str]] = defaultdict(list)
        self.converted_bindings: dict[str, str] = {}
        self.widget_replacements = 0
        self.listbox_template_needed = False
        self.widgets_left_unchanged = 0
        self.unsupported_widgets: dict[str, int] = defaultdict(int)
        self.converted_widget_types: dict[str, int] = defaultdict(int)
        self.unchanged_widget_types: dict[str, int] = defaultdict(int)
        self._class_target_stack: list[str | None] = []
        self.target_rules: dict[str, WidgetRule] = {}
        for rule in WIDGET_RULES.values():
            if rule.target_name and rule.target_name not in self.target_rules:
                self.target_rules[rule.target_name] = rule

    def _line(self, node: cst.CSTNode) -> int:
        try:
            return self.get_metadata(metadata.PositionProvider, node).start.line
        except KeyError:
            return 0

    def _column(self, node: cst.CSTNode) -> int:
        try:
            return self.get_metadata(metadata.PositionProvider, node).start.column + 1
        except KeyError:
            return 0

    def _warn(
        self,
        node: cst.CSTNode,
        message: str,
        *,
        category: str,
        symbol: str | None = None,
    ) -> None:
        line = self._line(node)
        diagnostic = Diagnostic(
            level=DiagnosticLevel.WARNING,
            message=message,
            category=category,
            line=line or None,
            column=(self._column(node) or None),
            symbol=symbol,
        )
        self.diagnostics.append(diagnostic)
        if message not in self.comments_by_line[line]:
            self.comments_by_line[line].append(message)

    def _expr_code(self, node: cst.CSTNode) -> str:
        return cst.Module([]).code_for_node(node)

    def _expr_key(self, node: cst.BaseExpression) -> str | None:
        if isinstance(node, cst.Name):
            return node.value
        if isinstance(node, cst.Attribute):
            return self._expr_code(node)
        return None

    def _literal_number(self, node: cst.BaseExpression) -> float | None:
        try:
            value = ast.literal_eval(self._expr_code(node))
        except Exception:
            return None
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def _resolve_name(self, node: cst.BaseExpression) -> str | None:
        return self.analysis.resolve_name(node)

    def _converted_target_name(self, call: cst.Call) -> str | None:
        if isinstance(call.func, cst.Attribute) and isinstance(call.func.value, cst.Name):
            if call.func.value.value == "ctk":
                return f"ctk.{call.func.attr.value}"
        if isinstance(call.func, cst.Name) and call.func.value == "CTkListbox":
            return "CTkListbox"
        return None

    def _in_definition_context(self, node: cst.Name) -> bool:
        parent = self.get_metadata(metadata.ParentNodeProvider, node)
        if isinstance(parent, (cst.ImportAlias, cst.AsName)):
            return True
        if isinstance(parent, cst.Attribute) and parent.attr is node:
            return True
        if isinstance(parent, cst.Param) and parent.name is node:
            return True
        if isinstance(parent, cst.FunctionDef) and parent.name is node:
            return True
        if isinstance(parent, cst.ClassDef) and parent.name is node:
            return True
        if isinstance(parent, cst.AssignTarget) and parent.target is node:
            return True
        if isinstance(parent, cst.AnnAssign) and parent.target is node:
            return True
        return False

    def _add_comment_lines(
        self,
        node: cst.SimpleStatementLine | cst.ClassDef,
        line: int,
    ) -> cst.SimpleStatementLine | cst.ClassDef:
        if not self.options.inline_todos:
            return node
        messages = self.comments_by_line.get(line, [])
        if not messages:
            return node
        existing_comments = {
            empty_line.comment.value
            for empty_line in node.leading_lines
            if empty_line.comment is not None
        }
        comment_lines = [
            cst.EmptyLine(comment=cst.Comment(f"# TODO tk2ctk: {message}"))
            for message in messages
            if f"# TODO tk2ctk: {message}" not in existing_comments
        ]
        if not comment_lines:
            return node
        return node.with_changes(leading_lines=[*comment_lines, *node.leading_lines])

    def _build_followup_statements(
        self,
        original_statement: cst.SimpleStatementLine,
        updated_statement: cst.SimpleStatementLine,
    ) -> list[cst.BaseStatement]:
        if len(original_statement.body) != 1 or len(updated_statement.body) != 1:
            return []

        original_small = original_statement.body[0]
        updated_small = updated_statement.body[0]
        if not isinstance(original_small, (cst.Assign, cst.AnnAssign)):
            return []
        if not isinstance(updated_small, (cst.Assign, cst.AnnAssign)):
            return []

        original_value = original_small.value
        updated_value = updated_small.value
        if not isinstance(original_value, cst.Call) or not isinstance(updated_value, cst.Call):
            return []

        resolved = self._resolve_name(original_value.func)
        if resolved is None:
            return []

        target_expr = None
        if isinstance(updated_small, cst.Assign):
            if len(updated_small.targets) == 1:
                target_expr = updated_small.targets[0].target
        elif isinstance(updated_small, cst.AnnAssign):
            target_expr = updated_small.target

        target_key = self._expr_key(target_expr) if target_expr is not None else None
        if not target_key:
            return []

        if resolved == "tk.OptionMenu" and len(original_value.args) >= 3:
            default_expr = original_value.args[2].value
            return [_stmt(f"{target_key}.set({self._expr_code(default_expr)})")]

        if resolved == "ttk.Progressbar":
            value_expr = None
            maximum_expr = None
            for argument in original_value.args:
                if argument.keyword is None:
                    continue
                if argument.keyword.value == "value":
                    value_expr = argument.value
                elif argument.keyword.value == "maximum":
                    maximum_expr = argument.value
            if value_expr is None:
                return []
            value = self._literal_number(value_expr)
            maximum = self._literal_number(maximum_expr) if maximum_expr else 100.0
            if value is None or maximum in (None, 0):
                return []
            return [_stmt(f"{target_key}.set({value / maximum!r})")]

        return []

    def _qualify_direct_name(self, name: str) -> cst.BaseExpression | None:
        if name in self.analysis.direct_tk_names:
            return _expr(f"tk.{self.analysis.direct_tk_names[name]}")
        if name in self.analysis.direct_ttk_names:
            return _expr(f"ttk.{self.analysis.direct_ttk_names[name]}")
        return None

    def _rewrite_args(
        self,
        original_node: cst.Call,
        updated_node: cst.Call,
        rule: WidgetRule,
        *,
        extra_drops: Iterable[str] = (),
        silent_drops: Iterable[str] = (),
    ) -> list[cst.Arg]:
        rewritten: list[cst.Arg] = []
        extra_drops = set(extra_drops)
        silent_drops = set(silent_drops)
        for original_arg, updated_arg in zip(original_node.args, updated_node.args):
            if original_arg.keyword is None:
                rewritten.append(updated_arg)
                continue

            keyword = original_arg.keyword.value
            if keyword in silent_drops:
                continue
            if keyword in extra_drops:
                self._warn(
                    original_arg,
                    f"Dropped unsupported option '{keyword}' when converting {rule.source_name}.",
                    category="unsupported_option",
                    symbol=rule.source_name,
                )
                continue

            option_rule = rule.option_rules.get(keyword)
            if option_rule and option_rule.drop:
                note = option_rule.note or f"Dropped unsupported option '{keyword}'."
                self._warn(
                    original_arg,
                    note,
                    category="unsupported_option",
                    symbol=rule.source_name,
                )
                continue

            new_keyword = option_rule.rename_to if option_rule and option_rule.rename_to else keyword
            if rule.allowed_options and new_keyword not in rule.allowed_options:
                self._warn(
                    original_arg,
                    f"Dropped unsupported option '{keyword}' when converting {rule.source_name}.",
                    category="unsupported_option",
                    symbol=rule.source_name,
                )
                continue

            rewritten.append(
                updated_arg.with_changes(
                    keyword=cst.Name(new_keyword),
                )
            )
        if rewritten:
            rewritten[-1] = rewritten[-1].with_changes(comma=cst.MaybeSentinel.DEFAULT)
        return rewritten

    def _convert_scale_call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call,
        rule: WidgetRule,
    ) -> cst.Call:
        converted_args = self._rewrite_args(
            original_node,
            updated_node,
            rule,
            silent_drops={"resolution"},
        )
        resolution_arg = None
        from_arg = None
        to_arg = None
        for argument in original_node.args:
            if argument.keyword is None:
                continue
            if argument.keyword.value == "resolution":
                resolution_arg = argument.value
            elif argument.keyword.value == "from_":
                from_arg = argument.value
            elif argument.keyword.value == "to":
                to_arg = argument.value

        if resolution_arg is not None:
            resolution = self._literal_number(resolution_arg)
            from_value = self._literal_number(from_arg) if from_arg is not None else None
            to_value = self._literal_number(to_arg) if to_arg is not None else None
            if None not in (resolution, from_value, to_value) and resolution not in (None, 0):
                steps = (to_value - from_value) / resolution
                if steps > 0 and abs(round(steps) - steps) < 1e-9:
                    converted_args = [
                        arg
                        for arg in converted_args
                        if not (arg.keyword and arg.keyword.value == "resolution")
                    ]
                    converted_args.append(
                        cst.Arg(keyword=cst.Name("number_of_steps"), value=_expr(str(int(round(steps)))))
                    )
                else:
                    converted_args = [
                        arg
                        for arg in converted_args
                        if not (arg.keyword and arg.keyword.value == "resolution")
                    ]
                    self._warn(
                        original_node,
                        "Dropped Scale resolution because it could not be converted safely to number_of_steps.",
                        category="scale_resolution",
                        symbol=rule.source_name,
                    )
            else:
                converted_args = [
                    arg
                    for arg in converted_args
                    if not (arg.keyword and arg.keyword.value == "resolution")
                ]
                self._warn(
                    original_node,
                    "Dropped Scale resolution because it depends on non-literal values.",
                    category="scale_resolution",
                    symbol=rule.source_name,
                )

        self.widget_replacements += 1
        self.converted_widget_types[rule.target_name or rule.source_name] += 1
        return updated_node.with_changes(func=_expr(rule.target_name), args=converted_args)

    def _convert_option_menu_call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call,
        rule: WidgetRule,
    ) -> cst.Call:
        positional = [argument for argument in original_node.args if argument.keyword is None]
        keyword_args = [argument for argument in original_node.args if argument.keyword is not None]
        if len(positional) < 3:
            self._warn(
                original_node,
                "Preserved tk.OptionMenu because its positional arguments do not match the standard signature.",
                category="unsupported_pattern",
                symbol=rule.source_name,
            )
            return updated_node.with_changes(func=_expr("tk.OptionMenu"))

        master_arg = updated_node.args[0]
        variable_arg = cst.Arg(keyword=cst.Name("variable"), value=updated_node.args[1].value)
        values_code = ", ".join(self._expr_code(argument.value) for argument in positional[2:])
        values_arg = cst.Arg(keyword=cst.Name("values"), value=_expr(f"[{values_code}]"))
        rewritten_args: list[cst.Arg] = [master_arg, variable_arg, values_arg]
        updated_keyword_args = [argument for argument in updated_node.args if argument.keyword is not None]
        for original_arg, updated_arg in zip(keyword_args, updated_keyword_args):
            keyword = original_arg.keyword.value
            option_rule = rule.option_rules.get(keyword)
            if option_rule and option_rule.drop:
                self._warn(
                    original_arg,
                    option_rule.note or f"Dropped unsupported option '{keyword}'.",
                    category="unsupported_option",
                    symbol=rule.source_name,
                )
                continue
            new_keyword = option_rule.rename_to if option_rule and option_rule.rename_to else keyword
            if rule.allowed_options and new_keyword not in rule.allowed_options:
                self._warn(
                    original_arg,
                    f"Dropped unsupported option '{keyword}' when converting {rule.source_name}.",
                    category="unsupported_option",
                    symbol=rule.source_name,
                )
                continue
            rewritten_args.append(updated_arg.with_changes(keyword=cst.Name(new_keyword)))
        if rewritten_args:
            rewritten_args[-1] = rewritten_args[-1].with_changes(comma=cst.MaybeSentinel.DEFAULT)
        self.widget_replacements += 1
        self.converted_widget_types[rule.target_name or rule.source_name] += 1
        return updated_node.with_changes(func=_expr(rule.target_name), args=rewritten_args)

    def _progressbar_is_safe(self, node: cst.Call) -> bool:
        has_variable = False
        has_value = False
        for argument in node.args:
            if argument.keyword is None:
                continue
            if argument.keyword.value == "variable":
                has_variable = True
            elif argument.keyword.value == "value":
                has_value = True
                if self._literal_number(argument.value) is None:
                    return False
            elif argument.keyword.value == "maximum" and self._literal_number(argument.value) is None:
                return False
        return not has_variable or not has_value

    def _convert_progressbar_call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call,
        rule: WidgetRule,
    ) -> cst.Call:
        if any(
            argument.keyword and argument.keyword.value == "variable"
            for argument in original_node.args
        ):
            self._warn(
                original_node,
                "Preserved ttk.Progressbar because variable-driven progress cannot be converted safely.",
                category="unsupported_pattern",
                symbol=rule.source_name,
            )
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[rule.source_name] += 1
            return updated_node.with_changes(func=_expr("ttk.Progressbar"))

        if not self._progressbar_is_safe(original_node):
            self._warn(
                original_node,
                "Preserved ttk.Progressbar because value/maximum are not statically safe to normalize.",
                category="unsupported_pattern",
                symbol=rule.source_name,
            )
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[rule.source_name] += 1
            return updated_node.with_changes(func=_expr("ttk.Progressbar"))

        rewritten_args = self._rewrite_args(
            original_node,
            updated_node,
            rule,
            silent_drops={"value", "maximum", "variable"},
        )
        self.widget_replacements += 1
        self.converted_widget_types[rule.target_name or rule.source_name] += 1
        return updated_node.with_changes(func=_expr(rule.target_name), args=rewritten_args)

    def _convert_listbox_call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call,
        rule: WidgetRule,
    ) -> cst.Call:
        if not self.options.convert_listboxes:
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[rule.source_name] += 1
            self._warn(
                original_node,
                "Preserved tk.Listbox. Re-run with --listboxes to inline a CTkListbox shim.",
                category="unsupported_widget",
                symbol=rule.source_name,
            )
            return updated_node.with_changes(func=_expr("tk.Listbox"))

        self.listbox_template_needed = True
        rewritten_args = self._rewrite_args(original_node, updated_node, rule)
        self.widget_replacements += 1
        self.converted_widget_types[rule.target_name or rule.source_name] += 1
        return updated_node.with_changes(func=cst.Name("CTkListbox"), args=rewritten_args)

    def _converted_reference_expression(
        self,
        original_node: cst.CSTNode,
        resolved: str,
    ) -> cst.BaseExpression | None:
        rule = get_widget_rule(resolved)
        if rule is None:
            return None
        if rule.category == "unsupported":
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[resolved] += 1
            self.unsupported_widgets[resolved] += 1
            self._warn(
                original_node,
                rule.unsupported_reason or f"Unsupported widget: {resolved}.",
                category="unsupported_widget",
                symbol=resolved,
            )
            return _expr(resolved)
        if rule.category == "special" and resolved == "tk.Listbox":
            if self.options.convert_listboxes:
                self.listbox_template_needed = True
                self.widget_replacements += 1
                self.converted_widget_types[rule.target_name or rule.source_name] += 1
                return cst.Name("CTkListbox")
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[resolved] += 1
            self._warn(
                original_node,
                "Preserved tk.Listbox. Re-run with --listboxes to inline a CTkListbox shim.",
                category="unsupported_widget",
                symbol=resolved,
            )
            return _expr("tk.Listbox")
        if rule.target_name:
            self.widget_replacements += 1
            self.converted_widget_types[rule.target_name or rule.source_name] += 1
            return _expr(rule.target_name)
        return None

    def _reference_context_allows_rewrite(self, node: cst.CSTNode) -> bool:
        parent = self.get_metadata(metadata.ParentNodeProvider, node)
        if isinstance(parent, cst.Call) and parent.func is node:
            return False
        if isinstance(parent, cst.ClassDef):
            return False
        if isinstance(parent, cst.ImportAlias):
            return False
        if isinstance(parent, cst.AsName):
            return False
        return True

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        converted_target: str | None = None
        for base in node.bases:
            resolved = self._resolve_name(base.value)
            if resolved is None:
                continue
            rule = get_widget_rule(resolved)
            if rule is not None and rule.target_name is not None and rule.category != "unsupported":
                converted_target = rule.target_name
                break
        self._class_target_stack.append(converted_target)

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import):
        remaining: list[cst.ImportAlias] = []
        for alias in updated_node.names:
            if isinstance(alias.name, cst.Name) and alias.name.value in {"tkinter", "customtkinter"}:
                continue
            if isinstance(alias.name, cst.Attribute):
                module_name = self._expr_code(alias.name)
                if module_name in {"tkinter.ttk", "customtkinter"}:
                    continue
            remaining.append(alias)
        if not remaining:
            return cst.RemoveFromParent()
        return updated_node.with_changes(names=remaining)

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom):
        module = None
        if isinstance(original_node.module, cst.Name):
            module = original_node.module.value
        elif isinstance(original_node.module, cst.Attribute):
            module = self._expr_code(original_node.module)

        if module not in {"tkinter", "tkinter.ttk", "customtkinter"}:
            return updated_node

        if isinstance(original_node.names, cst.ImportStar):
            self._warn(
                original_node,
                f"Preserved 'from {module} import *'. Wildcard imports are not normalized safely.",
                category="wildcard_import",
                symbol=module,
            )
            return updated_node
        return cst.RemoveFromParent()

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name):
        if self._in_definition_context(original_node):
            return updated_node

        if (
            isinstance(self.get_metadata(metadata.ParentNodeProvider, original_node), cst.Attribute)
            and original_node.value in self.analysis.tkinter_aliases
            and original_node.value != "tk"
        ):
            return cst.Name("tk")
        if (
            isinstance(self.get_metadata(metadata.ParentNodeProvider, original_node), cst.Attribute)
            and original_node.value in self.analysis.ttk_aliases
            and original_node.value != "ttk"
        ):
            return cst.Name("ttk")

        qualified = self._qualify_direct_name(original_node.value)
        if qualified is not None:
            resolved = self.analysis.resolve_name(cst.Name(original_node.value))
            if resolved in WIDGET_RULES and self._reference_context_allows_rewrite(original_node):
                converted = self._converted_reference_expression(original_node, resolved)
                if converted is not None:
                    return converted
            return qualified

        if original_node.value in TK_MODULE_NAMES:
            return _expr(f"tk.{original_node.value}")

        return updated_node

    def leave_Attribute(self, original_node: cst.Attribute, updated_node: cst.Attribute):
        resolved = self._resolve_name(original_node)
        if resolved is None:
            return updated_node

        if not self._reference_context_allows_rewrite(original_node):
            if isinstance(updated_node.value, cst.Name):
                if updated_node.value.value in self.analysis.tkinter_aliases and updated_node.value.value != "tk":
                    return updated_node.with_changes(value=cst.Name("tk"))
                if updated_node.value.value in self.analysis.ttk_aliases and updated_node.value.value != "ttk":
                    return updated_node.with_changes(value=cst.Name("ttk"))
            return updated_node

        if resolved in WIDGET_RULES:
            converted = self._converted_reference_expression(original_node, resolved)
            if converted is not None:
                return converted

        if isinstance(updated_node.value, cst.Name):
            if updated_node.value.value in self.analysis.tkinter_aliases and updated_node.value.value != "tk":
                return updated_node.with_changes(value=cst.Name("tk"))
            if updated_node.value.value in self.analysis.ttk_aliases and updated_node.value.value != "ttk":
                return updated_node.with_changes(value=cst.Name("ttk"))
        return updated_node

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef):
        updated_bases: list[cst.Arg] = []
        for original_base, updated_base in zip(original_node.bases, updated_node.bases):
            resolved = self._resolve_name(original_base.value)
            if resolved is None:
                updated_bases.append(updated_base)
                continue
            rule = get_widget_rule(resolved)
            if rule is None:
                updated_bases.append(updated_base)
                continue
            if rule.category == "unsupported":
                self.widgets_left_unchanged += 1
                self._warn(
                    original_base,
                    rule.unsupported_reason or f"Unsupported widget base {resolved}.",
                    category="unsupported_widget",
                    symbol=resolved,
                )
                self.unchanged_widget_types[resolved] += 1
                self.unsupported_widgets[resolved] += 1
                updated_bases.append(updated_base.with_changes(value=_expr(resolved)))
                continue
            if rule.category == "special" and resolved == "tk.Listbox" and not self.options.convert_listboxes:
                self.widgets_left_unchanged += 1
                self.unchanged_widget_types[resolved] += 1
                self._warn(
                    original_base,
                    "Preserved tk.Listbox base class because --listboxes was not enabled.",
                    category="unsupported_widget",
                    symbol=resolved,
                )
                updated_bases.append(updated_base.with_changes(value=_expr("tk.Listbox")))
                continue
            if rule.target_name:
                self.converted_widget_types[rule.target_name] += 1
                updated_bases.append(updated_base.with_changes(value=_expr(rule.target_name)))
                continue
            updated_bases.append(updated_base)

        updated_node = updated_node.with_changes(bases=updated_bases)
        updated_node = self._add_comment_lines(updated_node, self._line(original_node))
        self._class_target_stack.pop()
        return updated_node

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call):
        if isinstance(original_node.func, cst.Attribute):
            method_name = original_node.func.attr.value
            receiver_key = self._expr_key(original_node.func.value)
            if (
                method_name == "__init__"
                and isinstance(original_node.func.value, cst.Call)
                and isinstance(original_node.func.value.func, cst.Name)
                and original_node.func.value.func.value == "super"
                and self._class_target_stack
                and self._class_target_stack[-1] is not None
            ):
                rule = self.target_rules.get(self._class_target_stack[-1])
                if rule is not None:
                    rewritten_args = self._rewrite_args(original_node, updated_node, rule)
                    return updated_node.with_changes(args=rewritten_args)
            if method_name in {"config", "configure"} and receiver_key in self.converted_bindings:
                target_name = self.converted_bindings[receiver_key]
                rule = self.target_rules.get(target_name)
                rewritten_args = (
                    self._rewrite_args(original_node, updated_node, rule) if rule else list(updated_node.args)
                )
                return updated_node.with_changes(
                    func=updated_node.func.with_changes(attr=cst.Name("configure")),
                    args=rewritten_args,
                )

        resolved = self._resolve_name(original_node.func)
        if resolved is None:
            return updated_node

        rule = get_widget_rule(resolved)
        if rule is None:
            if resolved.startswith("tk.") or resolved.startswith("ttk."):
                return updated_node.with_changes(func=_expr(resolved))
            return updated_node

        if rule.category == "unsupported":
            self.widgets_left_unchanged += 1
            self.unchanged_widget_types[resolved] += 1
            self.unsupported_widgets[resolved] += 1
            self._warn(
                original_node,
                rule.unsupported_reason or f"Unsupported widget: {resolved}.",
                category="unsupported_widget",
                symbol=resolved,
            )
            return updated_node.with_changes(func=_expr(resolved))

        if rule.category == "special":
            if resolved in {"tk.Scale", "ttk.Scale"}:
                return self._convert_scale_call(original_node, updated_node, rule)
            if resolved == "tk.OptionMenu":
                return self._convert_option_menu_call(original_node, updated_node, rule)
            if resolved == "ttk.Progressbar":
                return self._convert_progressbar_call(original_node, updated_node, rule)
            if resolved == "tk.Listbox":
                return self._convert_listbox_call(original_node, updated_node, rule)

        rewritten_args = self._rewrite_args(original_node, updated_node, rule)
        self.widget_replacements += 1
        self.converted_widget_types[rule.target_name or rule.source_name] += 1
        return updated_node.with_changes(func=_expr(rule.target_name), args=rewritten_args)

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign):
        if isinstance(updated_node.value, cst.Call):
            converted_target = self._converted_target_name(updated_node.value)
            if converted_target:
                for assign_target in updated_node.targets:
                    key = self._expr_key(assign_target.target)
                    if key:
                        self.converted_bindings[key] = converted_target
        return updated_node

    def leave_AnnAssign(self, original_node: cst.AnnAssign, updated_node: cst.AnnAssign):
        if updated_node.value is not None and isinstance(updated_node.value, cst.Call):
            converted_target = self._converted_target_name(updated_node.value)
            if converted_target:
                key = self._expr_key(updated_node.target)
                if key:
                    self.converted_bindings[key] = converted_target
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ):
        line = self._line(original_node)
        updated_node = self._add_comment_lines(updated_node, line)
        followups = self._build_followup_statements(original_node, updated_node)
        if followups:
            return cst.FlattenSentinel([updated_node, *followups])
        return updated_node

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module):
        usage = ImportUsageCollector()
        updated_node.visit(usage)

        new_imports: list[cst.BaseStatement] = []
        if usage.uses_ctk or self.widget_replacements or self.listbox_template_needed:
            new_imports.append(_stmt("import customtkinter as ctk"))
        if usage.uses_tk:
            new_imports.append(_stmt("import tkinter as tk"))
        if usage.uses_ttk:
            new_imports.append(_stmt("from tkinter import ttk"))

        body = list(updated_node.body)
        insert_at = 0
        if body:
            first = body[0]
            if isinstance(first, cst.SimpleStatementLine) and len(first.body) == 1:
                expr = first.body[0]
                if isinstance(expr, cst.Expr) and isinstance(expr.value, cst.SimpleString):
                    insert_at = 1

        additions = list(new_imports)
        if self.listbox_template_needed:
            additions.extend(cst.parse_module(LISTBOX_TEMPLATE).body)

        if additions:
            body = [*body[:insert_at], *additions, *body[insert_at:]]

        return updated_node.with_changes(body=body)
