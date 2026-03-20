"""Public conversion service used by the CLI and SourceConverter facade."""

from __future__ import annotations

import difflib
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable

import libcst as cst
from libcst import metadata

from .analysis import analyze_imports
from .models import (
    ConversionOptions,
    ConversionReport,
    ConversionResult,
    Diagnostic,
    DiagnosticLevel,
    FileChange,
    RiskClass,
    with_path,
)
from .transformer import TkinterToCustomTkinterTransformer


RISK_ORDER = {
    RiskClass.SAFE: 0,
    RiskClass.REVIEW: 1,
    RiskClass.UNSAFE: 2,
}


def _diagnostic_counts(diagnostics: list[Diagnostic]) -> dict[str, int]:
    counts = Counter(diagnostic.level.value for diagnostic in diagnostics)
    return {
        DiagnosticLevel.INFO.value: counts.get(DiagnosticLevel.INFO.value, 0),
        DiagnosticLevel.WARNING.value: counts.get(DiagnosticLevel.WARNING.value, 0),
        DiagnosticLevel.ERROR.value: counts.get(DiagnosticLevel.ERROR.value, 0),
    }


def _classify_risk(
    *,
    diagnostics: list[Diagnostic],
    unsupported_widget_count: int,
    options: ConversionOptions,
) -> RiskClass:
    severity_counts = _diagnostic_counts(diagnostics)
    warning_count = severity_counts[DiagnosticLevel.WARNING.value]
    error_count = severity_counts[DiagnosticLevel.ERROR.value]
    if error_count:
        return RiskClass.UNSAFE
    if warning_count > options.max_warnings:
        return RiskClass.UNSAFE
    if unsupported_widget_count > options.max_unsupported:
        return RiskClass.UNSAFE
    if warning_count or unsupported_widget_count:
        return RiskClass.REVIEW
    return RiskClass.SAFE


def _worst_risk(risk_classes: Iterable[RiskClass]) -> RiskClass:
    worst = RiskClass.SAFE
    for risk_class in risk_classes:
        if RISK_ORDER[risk_class] > RISK_ORDER[worst]:
            worst = risk_class
    return worst


def _build_report(
    *,
    files_scanned: int = 0,
    files_processed: int = 0,
    files_changed: int = 0,
    files_skipped: int = 0,
    files_failed: int = 0,
    risk_class: RiskClass = RiskClass.SAFE,
    files_by_risk: dict[str, int] | None = None,
    widgets_converted: int = 0,
    widgets_left_unchanged: int = 0,
    widgets_converted_by_type: dict[str, int] | None = None,
    widgets_left_unchanged_by_type: dict[str, int] | None = None,
    unsupported_widgets: dict[str, int] | None = None,
    diagnostics_by_severity: dict[str, int] | None = None,
    warnings_by_category: dict[str, int] | None = None,
    file_changes: list[FileChange] | None = None,
) -> ConversionReport:
    unsupported_widgets = unsupported_widgets or {}
    diagnostics_by_severity = diagnostics_by_severity or {}
    return ConversionReport(
        files_scanned=files_scanned,
        files_processed=files_processed,
        files_changed=files_changed,
        files_skipped=files_skipped,
        files_failed=files_failed,
        risk_class=risk_class,
        files_by_risk=files_by_risk or {},
        widgets_converted=widgets_converted,
        widgets_left_unchanged=widgets_left_unchanged,
        widgets_converted_by_type=widgets_converted_by_type or {},
        widgets_left_unchanged_by_type=widgets_left_unchanged_by_type or {},
        unsupported_widgets=unsupported_widgets,
        unsupported_widget_count=sum(unsupported_widgets.values()),
        warnings_emitted=sum((warnings_by_category or {}).values()),
        diagnostics_by_severity=diagnostics_by_severity,
        warnings_by_category=warnings_by_category or {},
        file_changes=file_changes or [],
    )


def _error_result(source: str, message: str, category: str) -> ConversionResult:
    diagnostic = Diagnostic(
        level=DiagnosticLevel.ERROR,
        message=message,
        category=category,
    )
    diagnostics = [diagnostic]
    return ConversionResult(
        source=source,
        diagnostics=diagnostics,
        success=False,
        changed=False,
        risk_class=RiskClass.UNSAFE,
        should_review=True,
        report=_build_report(
            files_failed=1,
            risk_class=RiskClass.UNSAFE,
            files_by_risk={RiskClass.UNSAFE.value: 1},
            diagnostics_by_severity=_diagnostic_counts(diagnostics),
        ),
    )


def convert_source(source: str, options: ConversionOptions | None = None) -> ConversionResult:
    """Convert tkinter source code into customtkinter source code."""

    options = options or ConversionOptions()
    try:
        module = cst.parse_module(source)
    except Exception as exc:
        return _error_result(source, f"Failed to parse source: {exc}", "parse_error")

    try:
        analysis = analyze_imports(module)
        wrapper = metadata.MetadataWrapper(module)
        transformer = TkinterToCustomTkinterTransformer(analysis, options)
        transformed = wrapper.visit(transformer)
    except Exception as exc:
        return _error_result(source, f"Unexpected transformer failure: {exc}", "transform_error")

    todo_count = sum(len(messages) for messages in transformer.comments_by_line.values())
    warning_categories = Counter(
        diagnostic.category
        for diagnostic in transformer.diagnostics
        if diagnostic.level == DiagnosticLevel.WARNING
    )
    diagnostics_by_severity = _diagnostic_counts(transformer.diagnostics)
    converted_by_type = dict(transformer.converted_widget_types)
    unchanged_by_type = dict(transformer.unchanged_widget_types)
    unsupported_widgets = dict(transformer.unsupported_widgets)
    risk_class = _classify_risk(
        diagnostics=transformer.diagnostics,
        unsupported_widget_count=sum(unsupported_widgets.values()),
        options=options,
    )
    report = _build_report(
        risk_class=risk_class,
        files_by_risk={risk_class.value: 1},
        widgets_converted=sum(converted_by_type.values()),
        widgets_left_unchanged=sum(unchanged_by_type.values()),
        widgets_converted_by_type=converted_by_type,
        widgets_left_unchanged_by_type=unchanged_by_type,
        unsupported_widgets=unsupported_widgets,
        diagnostics_by_severity=diagnostics_by_severity,
        warnings_by_category=dict(warning_categories),
    )
    return ConversionResult(
        source=transformed.code,
        diagnostics=transformer.diagnostics,
        widget_replacements=transformer.widget_replacements,
        todo_comments=todo_count,
        changed=transformed.code != source,
        success=True,
        risk_class=risk_class,
        should_review=risk_class != RiskClass.SAFE,
        report=report,
    )


def _unified_diff(original: str, updated: str, *, fromfile: str, tofile: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            original.splitlines(),
            updated.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    )


def _write_atomic(path: Path, content: str, *, backup: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        if backup and path.exists():
            backup_path = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, backup_path)
        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def _output_path_for_single(
    input_path: Path,
    output_path: str | Path | None,
    options: ConversionOptions,
) -> Path:
    if options.write_in_place:
        return input_path
    if output_path is not None:
        return Path(output_path)
    if options.output_dir:
        return Path(options.output_dir) / input_path.name
    return input_path.parent / f"customtkinter_{input_path.name}"


def convert_file(
    input_path: str | Path,
    output_path: str | Path | None = None,
    options: ConversionOptions | None = None,
) -> ConversionResult:
    """Convert a file on disk and optionally write the transformed result."""

    options = options or ConversionOptions()
    input_path = Path(input_path)
    try:
        original_source = input_path.read_text(encoding="utf-8")
    except Exception as exc:
        result = _error_result("", f"Failed to read file: {exc}", "file_io")
        result.input_path = str(input_path)
        result.diagnostics = with_path(input_path, result.diagnostics)
        result.report = _build_report(
            files_scanned=1,
            files_processed=1,
            files_failed=1,
            risk_class=RiskClass.UNSAFE,
            files_by_risk={RiskClass.UNSAFE.value: 1},
            diagnostics_by_severity=_diagnostic_counts(result.diagnostics),
            warnings_by_category={},
            file_changes=[
                FileChange(
                    input_path=str(input_path),
                    success=False,
                    reason="read_failed",
                    risk_class=RiskClass.UNSAFE,
                    should_review=True,
                    diagnostics_by_severity=_diagnostic_counts(result.diagnostics),
                    diagnostics=result.diagnostics,
                )
            ],
        )
        return result

    result = convert_source(original_source, options=options)
    result.input_path = str(input_path)
    result.diagnostics = with_path(input_path, result.diagnostics)
    result.changed = result.source != original_source

    destination = _output_path_for_single(input_path, output_path, options)
    result.output_path = str(destination)
    if result.changed:
        result.diff = _unified_diff(
            original_source,
            result.source,
            fromfile=str(input_path),
            tofile=str(destination),
        )

    file_change = FileChange(
        input_path=str(input_path),
        output_path=str(destination),
        changed=result.changed,
        skipped=not result.changed,
        success=result.success,
        reason=None if result.success else "conversion_failed",
        risk_class=result.risk_class,
        should_review=result.risk_class != RiskClass.SAFE,
        widget_replacements=result.report.widgets_converted,
        todo_comments=result.todo_comments,
        unsupported_widget_count=result.report.unsupported_widget_count,
        diagnostics_by_severity=dict(result.report.diagnostics_by_severity),
        widgets_converted_by_type=dict(result.report.widgets_converted_by_type),
        widgets_left_unchanged_by_type=dict(result.report.widgets_left_unchanged_by_type),
        unsupported_widgets_by_type=dict(result.report.unsupported_widgets),
        warnings_by_category=dict(result.report.warnings_by_category),
        diagnostics=result.diagnostics,
        diff=result.diff,
    )

    risk_filtered = bool(options.risk_filters and result.risk_class not in options.risk_filters)
    write_blocked = False
    if (
        result.success
        and result.changed
        and not options.dry_run
        and risk_filtered
    ):
        write_blocked = True
        result.skipped = True
        file_change.skipped = True
        file_change.reason = "risk_filtered"
    elif (
        result.success
        and result.changed
        and not options.dry_run
        and options.write_in_place
        and result.risk_class == RiskClass.UNSAFE
        and not options.allow_unsafe_write
    ):
        write_blocked = True
        result.skipped = True
        file_change.skipped = True
        file_change.reason = "unsafe_write_blocked"
    elif result.success and result.changed and not options.dry_run:
        try:
            _write_atomic(destination, result.source, backup=options.backup)
        except Exception as exc:
            error = Diagnostic(
                level=DiagnosticLevel.ERROR,
                message=f"Failed to write output: {exc}",
                category="file_io",
                path=str(input_path),
            )
            result.diagnostics.append(error)
            result.success = False
            file_change.success = False
            file_change.reason = "write_failed"
            file_change.diagnostics = result.diagnostics

    if result.success and not result.changed:
        result.skipped = True
        file_change.skipped = True
        file_change.reason = "unchanged"
    elif result.success and options.dry_run:
        file_change.reason = "dry_run"
    elif write_blocked and not file_change.reason:
        file_change.reason = "unsafe_write_blocked"

    severity_counts = _diagnostic_counts(result.diagnostics)
    unsupported_widget_count = sum(result.report.unsupported_widgets.values())
    result.risk_class = _classify_risk(
        diagnostics=result.diagnostics,
        unsupported_widget_count=unsupported_widget_count,
        options=options,
    )
    result.should_review = result.risk_class != RiskClass.SAFE
    file_change.risk_class = result.risk_class
    file_change.should_review = result.should_review
    file_change.unsupported_widget_count = unsupported_widget_count
    file_change.diagnostics_by_severity = severity_counts
    warning_categories = Counter(
        diagnostic.category
        for diagnostic in result.diagnostics
        if diagnostic.level == DiagnosticLevel.WARNING
    )
    result.report = _build_report(
        files_scanned=1,
        files_processed=1,
        files_changed=1 if result.success and result.changed else 0,
        files_skipped=1 if file_change.skipped else 0,
        files_failed=0 if result.success else 1,
        risk_class=result.risk_class,
        files_by_risk={result.risk_class.value: 1},
        widgets_converted=result.report.widgets_converted,
        widgets_left_unchanged=result.report.widgets_left_unchanged,
        widgets_converted_by_type=dict(result.report.widgets_converted_by_type),
        widgets_left_unchanged_by_type=dict(result.report.widgets_left_unchanged_by_type),
        unsupported_widgets=dict(result.report.unsupported_widgets),
        diagnostics_by_severity=severity_counts,
        warnings_by_category=dict(warning_categories),
        file_changes=[file_change],
    )
    return result


def _matches_any(path_text: str, patterns: tuple[str, ...]) -> bool:
    return any(Path(path_text).match(pattern) for pattern in patterns)


def discover_python_files(paths: Iterable[str | Path], options: ConversionOptions) -> list[Path]:
    """Discover Python files from file and directory inputs."""

    discovered: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file():
            discovered.append(path)
            continue
        if not path.is_dir():
            continue
        iterator = path.rglob("*.py") if options.recursive else path.glob("*.py")
        for item in iterator:
            relative_text = str(item.relative_to(path))
            if options.include_patterns and not _matches_any(relative_text, options.include_patterns):
                continue
            if options.exclude_patterns and _matches_any(relative_text, options.exclude_patterns):
                continue
            discovered.append(item)
    return sorted({item.resolve() for item in discovered})


def _project_output_path(
    input_path: Path,
    base_path: Path,
    *,
    output_dir: Path | None,
    write_in_place: bool,
) -> Path:
    if write_in_place:
        return input_path
    if output_dir is None:
        return input_path.parent / f"customtkinter_{input_path.name}"
    return output_dir / input_path.relative_to(base_path)


def convert_paths(
    paths: Iterable[str | Path],
    options: ConversionOptions | None = None,
) -> ConversionReport:
    """Convert a collection of files or directories and return a project report."""

    options = options or ConversionOptions()
    path_list = [Path(path) for path in paths]
    discovered_files = discover_python_files(path_list, options)
    file_changes: list[FileChange] = []
    widgets_converted_by_type: Counter[str] = Counter()
    widgets_left_unchanged_by_type: Counter[str] = Counter()
    unsupported_widgets: Counter[str] = Counter()
    warnings_by_category: Counter[str] = Counter()
    diagnostics_by_severity: Counter[str] = Counter()
    files_by_risk: Counter[str] = Counter()

    output_dir = Path(options.output_dir) if options.output_dir else None
    if output_dir is not None and not options.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in discovered_files:
        base_path = next(
            (candidate for candidate in path_list if candidate.is_dir() and input_path.is_relative_to(candidate.resolve())),
            input_path.parent,
        )
        output_path = _project_output_path(
            input_path,
            base_path.resolve() if isinstance(base_path, Path) else input_path.parent,
            output_dir=output_dir,
            write_in_place=options.write_in_place,
        )
        result = convert_file(input_path, output_path=output_path, options=options)
        file_change = result.report.file_changes[0]
        file_changes.append(file_change)
        widgets_converted_by_type.update(file_change.widgets_converted_by_type)
        widgets_left_unchanged_by_type.update(file_change.widgets_left_unchanged_by_type)
        unsupported_widgets.update(file_change.unsupported_widgets_by_type)
        warnings_by_category.update(file_change.warnings_by_category)
        diagnostics_by_severity.update(file_change.diagnostics_by_severity)
        files_by_risk[file_change.risk_class.value] += 1

    project_risk = _worst_risk(
        RiskClass(name)
        for name, count in files_by_risk.items()
        for _ in range(count)
    )

    return _build_report(
        files_scanned=len(discovered_files),
        files_processed=len(file_changes),
        files_changed=sum(1 for item in file_changes if item.changed and item.success),
        files_skipped=sum(1 for item in file_changes if item.skipped),
        files_failed=sum(1 for item in file_changes if not item.success),
        risk_class=project_risk,
        files_by_risk=dict(files_by_risk),
        widgets_converted=sum(widgets_converted_by_type.values()),
        widgets_left_unchanged=sum(widgets_left_unchanged_by_type.values()),
        widgets_converted_by_type=dict(widgets_converted_by_type),
        widgets_left_unchanged_by_type=dict(widgets_left_unchanged_by_type),
        unsupported_widgets=dict(unsupported_widgets),
        diagnostics_by_severity=dict(diagnostics_by_severity),
        warnings_by_category=dict(warnings_by_category),
        file_changes=file_changes,
    )
