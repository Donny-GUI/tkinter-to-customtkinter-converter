"""Core types for tkinter-to-customtkinter conversion."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping


class DiagnosticLevel(StrEnum):
    """Severity levels emitted during conversion."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class RiskClass(StrEnum):
    """Operational safety class for a converted file or batch."""

    SAFE = "safe"
    REVIEW = "review"
    UNSAFE = "unsafe"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A structured message about an unsafe or unsupported conversion."""

    level: DiagnosticLevel
    message: str
    category: str
    line: int | None = None
    column: int | None = None
    symbol: str | None = None
    path: str | None = None


@dataclass(frozen=True, slots=True)
class OptionRule:
    """A per-keyword rewrite rule."""

    rename_to: str | None = None
    drop: bool = False
    note: str | None = None


@dataclass(frozen=True, slots=True)
class WidgetRule:
    """A widget conversion rule."""

    source_name: str
    target_name: str | None
    category: str = "direct"
    option_rules: Mapping[str, OptionRule] = field(default_factory=dict)
    allowed_options: frozenset[str] = field(default_factory=frozenset)
    unsupported_reason: str | None = None


@dataclass(frozen=True, slots=True)
class ConversionOptions:
    """Runtime options for a conversion pass."""

    convert_listboxes: bool = False
    verbose: bool = False
    inline_todos: bool = True
    report: bool = False
    recursive: bool = False
    include_patterns: tuple[str, ...] = ("*.py",)
    exclude_patterns: tuple[str, ...] = ()
    dry_run: bool = False
    show_diff: bool = False
    write_in_place: bool = False
    output_dir: str | None = None
    backup: bool = False
    json_report_path: str | None = None
    max_warnings: int = 10
    max_unsupported: int = 3
    fail_on_unsafe: bool = False
    fail_on_review: bool = False
    risk_filters: frozenset[RiskClass] = field(default_factory=frozenset)
    allow_unsafe_write: bool = False


@dataclass(slots=True)
class FileChange:
    """One file-level conversion outcome."""

    input_path: str
    output_path: str | None = None
    changed: bool = False
    skipped: bool = False
    success: bool = True
    reason: str | None = None
    risk_class: RiskClass = RiskClass.SAFE
    should_review: bool = False
    widget_replacements: int = 0
    todo_comments: int = 0
    unsupported_widget_count: int = 0
    diagnostics_by_severity: dict[str, int] = field(default_factory=dict)
    widgets_converted_by_type: dict[str, int] = field(default_factory=dict)
    widgets_left_unchanged_by_type: dict[str, int] = field(default_factory=dict)
    unsupported_widgets_by_type: dict[str, int] = field(default_factory=dict)
    warnings_by_category: dict[str, int] = field(default_factory=dict)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    diff: str = ""


@dataclass(slots=True)
class ConversionReport:
    """Structured summary of a conversion run."""

    files_scanned: int = 0
    files_processed: int = 0
    files_changed: int = 0
    files_skipped: int = 0
    files_failed: int = 0
    risk_class: RiskClass = RiskClass.SAFE
    files_by_risk: dict[str, int] = field(default_factory=dict)
    widgets_left_unchanged: int = 0
    widgets_converted: int = 0
    widgets_converted_by_type: dict[str, int] = field(default_factory=dict)
    widgets_left_unchanged_by_type: dict[str, int] = field(default_factory=dict)
    unsupported_widgets: dict[str, int] = field(default_factory=dict)
    unsupported_widget_count: int = 0
    warnings_emitted: int = 0
    diagnostics_by_severity: dict[str, int] = field(default_factory=dict)
    warnings_by_category: dict[str, int] = field(default_factory=dict)
    file_changes: list[FileChange] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert the report into a JSON-serializable dictionary."""

        return asdict(self)


@dataclass(slots=True)
class ConversionResult:
    """Full output from a conversion pass."""

    source: str
    diagnostics: list[Diagnostic]
    input_path: str | None = None
    output_path: str | None = None
    widget_replacements: int = 0
    todo_comments: int = 0
    changed: bool = False
    success: bool = True
    skipped: bool = False
    risk_class: RiskClass = RiskClass.SAFE
    should_review: bool = False
    diff: str = ""
    report: ConversionReport = field(default_factory=ConversionReport)


def with_path(path: str | Path, diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    """Attach a filesystem path to diagnostics."""

    path_str = str(path)
    return [
        Diagnostic(
            level=diagnostic.level,
            message=diagnostic.message,
            category=diagnostic.category,
            line=diagnostic.line,
            column=diagnostic.column,
            symbol=diagnostic.symbol,
            path=path_str,
        )
        for diagnostic in diagnostics
    ]
