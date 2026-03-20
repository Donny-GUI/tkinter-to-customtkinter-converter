"""Helpers for converter diagnostics."""

from __future__ import annotations

from collections import Counter

from .models import ConversionReport, Diagnostic, DiagnosticLevel


def format_diagnostic(diagnostic: Diagnostic) -> str:
    """Render a diagnostic for CLI output."""

    location = ""
    if diagnostic.path:
        location = f"{diagnostic.path}: "
    if diagnostic.line is not None:
        line_location = f"{diagnostic.line}"
        if diagnostic.column is not None:
            line_location += f":{diagnostic.column}"
        location += f"line {line_location}: "
    return f"[{diagnostic.level.upper()}] {diagnostic.category}: {location}{diagnostic.message}"


def summarize_diagnostics(diagnostics: list[Diagnostic]) -> dict[str, int]:
    """Count diagnostics by severity."""

    counts = Counter(diagnostic.level for diagnostic in diagnostics)
    return {
        DiagnosticLevel.INFO: counts.get(DiagnosticLevel.INFO, 0),
        DiagnosticLevel.WARNING: counts.get(DiagnosticLevel.WARNING, 0),
        DiagnosticLevel.ERROR: counts.get(DiagnosticLevel.ERROR, 0),
    }


def format_report(report: ConversionReport) -> list[str]:
    """Render a conversion report for CLI output."""

    lines = [
        f"files scanned: {report.files_scanned}",
        f"files processed: {report.files_processed}",
        f"files changed: {report.files_changed}",
        f"files skipped: {report.files_skipped}",
        f"files failed: {report.files_failed}",
        f"risk class: {report.risk_class}",
        f"widgets converted: {report.widgets_converted}",
        f"widgets left unchanged: {report.widgets_left_unchanged}",
        f"unsupported widget count: {report.unsupported_widget_count}",
        f"warnings emitted: {report.warnings_emitted}",
    ]
    if report.diagnostics_by_severity:
        details = ", ".join(
            f"{name}={count}" for name, count in sorted(report.diagnostics_by_severity.items())
        )
        lines.append(f"diagnostics by severity: {details}")
    if report.files_by_risk:
        details = ", ".join(
            f"{name}={count}" for name, count in sorted(report.files_by_risk.items())
        )
        lines.append(f"files by risk: {details}")
    if report.widgets_converted_by_type:
        details = ", ".join(
            f"{name}={count}" for name, count in sorted(report.widgets_converted_by_type.items())
        )
        lines.append(f"widgets converted by type: {details}")
    if report.warnings_by_category:
        details = ", ".join(
            f"{name}={count}" for name, count in sorted(report.warnings_by_category.items())
        )
        lines.append(f"warnings by category: {details}")
    if report.unsupported_widgets:
        details = ", ".join(
            f"{name}={count}" for name, count in sorted(report.unsupported_widgets.items())
        )
        lines.append(f"unsupported widgets: {details}")
    else:
        lines.append("unsupported widgets: none")
    return lines
