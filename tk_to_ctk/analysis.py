"""Import and symbol analysis for tkinter source modules."""

from __future__ import annotations

from dataclasses import dataclass, field

import libcst as cst


@dataclass(slots=True)
class ImportAnalysis:
    """Resolved import aliases used by the source module."""

    tkinter_aliases: set[str] = field(default_factory=set)
    ttk_aliases: set[str] = field(default_factory=set)
    direct_tk_names: dict[str, str] = field(default_factory=dict)
    direct_ttk_names: dict[str, str] = field(default_factory=dict)
    wildcard_tk_import: bool = False
    wildcard_ttk_import: bool = False

    def resolve_name(self, node: cst.BaseExpression) -> str | None:
        """Resolve a CST expression to a normalized tkinter/ttk name."""

        if isinstance(node, cst.Name):
            if node.value in self.direct_tk_names:
                return f"tk.{self.direct_tk_names[node.value]}"
            if node.value in self.direct_ttk_names:
                return f"ttk.{self.direct_ttk_names[node.value]}"
            return None

        if isinstance(node, cst.Attribute) and isinstance(node.value, cst.Name):
            module_name = node.value.value
            attribute_name = node.attr.value
            if module_name in self.tkinter_aliases:
                return f"tk.{attribute_name}"
            if module_name in self.ttk_aliases:
                return f"ttk.{attribute_name}"
        return None


class ImportAnalyzer(cst.CSTVisitor):
    """Collect import aliases that refer to tkinter and ttk."""

    def __init__(self) -> None:
        self.analysis = ImportAnalysis()

    def visit_Import(self, node: cst.Import) -> None:
        for alias in node.names:
            if not isinstance(alias, cst.ImportAlias):
                continue
            if isinstance(alias.name, cst.Name) and alias.name.value == "tkinter":
                asname = alias.asname.name.value if alias.asname else "tkinter"
                self.analysis.tkinter_aliases.add(asname)
            elif isinstance(alias.name, cst.Attribute):
                module_name = cst.Module([]).code_for_node(alias.name)
                if module_name == "tkinter.ttk":
                    asname = alias.asname.name.value if alias.asname else "ttk"
                    self.analysis.ttk_aliases.add(asname)

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        module = None
        if isinstance(node.module, cst.Name):
            module = node.module.value
        elif isinstance(node.module, cst.Attribute):
            module = cst.Module([]).code_for_node(node.module)

        if isinstance(node.names, cst.ImportStar):
            if module == "tkinter":
                self.analysis.wildcard_tk_import = True
            elif module == "tkinter.ttk":
                self.analysis.wildcard_ttk_import = True
            return

        for alias in node.names:
            imported_name = cst.Module([]).code_for_node(alias.name)
            local_name = alias.asname.name.value if alias.asname else imported_name
            if module == "tkinter":
                if imported_name == "ttk":
                    self.analysis.ttk_aliases.add(local_name)
                else:
                    self.analysis.direct_tk_names[local_name] = imported_name
            elif module == "tkinter.ttk":
                self.analysis.direct_ttk_names[local_name] = imported_name


def analyze_imports(module: cst.Module) -> ImportAnalysis:
    """Analyze tkinter-related imports in a module."""

    visitor = ImportAnalyzer()
    module.visit(visitor)
    if not visitor.analysis.tkinter_aliases and (
        visitor.analysis.direct_tk_names or visitor.analysis.wildcard_tk_import
    ):
        visitor.analysis.tkinter_aliases.add("tk")
    if not visitor.analysis.ttk_aliases and (
        visitor.analysis.direct_ttk_names or visitor.analysis.wildcard_ttk_import
    ):
        visitor.analysis.ttk_aliases.add("ttk")
    return visitor.analysis
