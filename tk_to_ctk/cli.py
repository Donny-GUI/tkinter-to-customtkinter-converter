"""Command-line interface for tkinter-to-customtkinter conversion."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ._version import __version__
from .diagnostics import format_diagnostic, format_report
from .models import ConversionOptions, ConversionReport, FileChange, RiskClass
from .service import convert_file, convert_paths


def get_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Convert Tkinter scripts to CustomTkinter scripts",
        prog="tk2ctk",
        usage="tk2ctk [TARGET] [options]",
        add_help=False,
        exit_on_error=False,
    )
    parser.add_argument("Target", default=None, metavar="TARGET", nargs="?")
    parser.add_argument("-h", "--help", dest="Help", default=False, action="store_true")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-o", "--outfile", dest="Output", default=None, nargs="?")
    parser.add_argument("--output-dir", dest="OutputDir", default=None)
    parser.add_argument("--in-place", dest="InPlace", default=False, action="store_true")
    parser.add_argument("--recursive", dest="Recursive", default=False, action="store_true")
    parser.add_argument("--include", dest="Includes", action="append", default=[])
    parser.add_argument("--exclude", dest="Excludes", action="append", default=[])
    parser.add_argument("--dry-run", dest="DryRun", default=False, action="store_true")
    parser.add_argument("--diff", dest="Diff", default=False, action="store_true")
    parser.add_argument("--backup", dest="Backup", default=False, action="store_true")
    parser.add_argument("--allow-unsafe-write", dest="AllowUnsafeWrite", default=False, action="store_true")
    parser.add_argument("--max-warnings", dest="MaxWarnings", type=int, default=10)
    parser.add_argument("--max-unsupported", dest="MaxUnsupported", type=int, default=3)
    parser.add_argument("--fail-on-unsafe", dest="FailOnUnsafe", default=False, action="store_true")
    parser.add_argument("--fail-on-review", dest="FailOnReview", default=False, action="store_true")
    risk_group = parser.add_mutually_exclusive_group()
    risk_group.add_argument("--only-safe", dest="OnlySafe", default=False, action="store_true")
    risk_group.add_argument("--only-review", dest="OnlyReview", default=False, action="store_true")
    risk_group.add_argument("--only-unsafe", dest="OnlyUnsafe", default=False, action="store_true")
    parser.add_argument("--json-report", dest="JsonReport", default=None, nargs="?", const="-")
    parser.add_argument("-v", "--verbose", dest="Verbose", default=False, action="store_true")
    parser.add_argument("-l", "--listboxes", dest="Listboxes", default=False, action="store_true")
    parser.add_argument("-m", "--multiple", dest="Multiple", default=[], nargs="+")
    parser.add_argument("-e", "--examples", dest="Examples", default=False, action="store_true")
    parser.add_argument("-r", "--report", dest="Report", default=False, action="store_true")
    return parser


def print_examples() -> None:
    """Print CLI examples."""

    print("Examples:")
    print("  tk2ctk app.py")
    print("  tk2ctk app.py --diff")
    print("  tk2ctk src --recursive --dry-run --report")
    print("  tk2ctk src --recursive --output-dir converted --json-report report.json")
    print("  tk2ctk src --recursive --in-place --backup")
    print("  tk2ctk -m app1.py app2.py --in-place")


def input_filename_to_output_filename(input_filename: str) -> str:
    """Match the historic default output naming convention."""

    return os.path.join(
        os.getcwd(),
        "customtkinter_" + os.path.basename(str(input_filename)),
    )


def _options_from_args(args: argparse.Namespace) -> ConversionOptions:
    risk_filters: frozenset[RiskClass] = frozenset()
    if args.OnlySafe:
        risk_filters = frozenset({RiskClass.SAFE})
    elif args.OnlyReview:
        risk_filters = frozenset({RiskClass.REVIEW})
    elif args.OnlyUnsafe:
        risk_filters = frozenset({RiskClass.UNSAFE})
    return ConversionOptions(
        convert_listboxes=args.Listboxes,
        verbose=args.Verbose,
        report=args.Report,
        recursive=args.Recursive,
        include_patterns=tuple(args.Includes or ("*.py",)),
        exclude_patterns=tuple(args.Excludes),
        dry_run=args.DryRun,
        show_diff=args.Diff,
        write_in_place=args.InPlace,
        output_dir=args.OutputDir,
        backup=args.Backup,
        json_report_path=args.JsonReport,
        max_warnings=args.MaxWarnings,
        max_unsupported=args.MaxUnsupported,
        fail_on_unsafe=args.FailOnUnsafe,
        fail_on_review=args.FailOnReview,
        risk_filters=risk_filters,
        allow_unsafe_write=args.AllowUnsafeWrite,
    )


def _print_file_change(change: FileChange, *, show_diff: bool = False) -> None:
    status = "FAILED"
    if change.success:
        status = "CHANGED" if change.changed else "SKIPPED"
    print(f"[{status}][{change.risk_class.upper()}] {change.input_path}")
    if change.output_path and change.output_path != change.input_path:
        print(f"[UPDATE] output: {change.output_path}")
    if change.reason and change.reason not in {"unchanged", "dry_run"}:
        print(f"[UPDATE] reason: {change.reason}")
    severity_details = ", ".join(
        f"{name}={count}" for name, count in sorted(change.diagnostics_by_severity.items())
    ) or "none"
    print(
        "[UPDATE] "
        f"risk={change.risk_class} "
        f"manual_review={'yes' if change.should_review else 'no'} "
        f"unsupported={change.unsupported_widget_count} "
        f"diagnostics={severity_details}"
    )
    for diagnostic in change.diagnostics:
        print(format_diagnostic(diagnostic))
    if show_diff and change.diff:
        print(change.diff)


def _emit_json_report(report: ConversionReport, destination: str | None) -> None:
    if destination is None:
        return
    payload = json.dumps(report.to_dict(), indent=2)
    if destination == "-":
        print(payload)
        return
    Path(destination).write_text(payload, encoding="utf-8")


def _print_report(report: ConversionReport) -> None:
    for line in format_report(report):
        print(f"[UPDATE] {line}")


def _exit_code_for_report(report: ConversionReport, options: ConversionOptions) -> int:
    if report.files_failed:
        return 1
    if options.fail_on_unsafe and report.files_by_risk.get(RiskClass.UNSAFE.value, 0):
        return 1
    if options.fail_on_review and (
        report.files_by_risk.get(RiskClass.REVIEW.value, 0)
        or report.files_by_risk.get(RiskClass.UNSAFE.value, 0)
    ):
        return 1
    return 0


def _handle_single_file(target: Path, args: argparse.Namespace) -> int:
    options = _options_from_args(args)
    output = args.Output
    if output is None and not args.InPlace and not args.OutputDir:
        output = input_filename_to_output_filename(str(target))
    result = convert_file(target, output_path=output, options=options)
    change = result.report.file_changes[0]
    _print_file_change(change, show_diff=args.Diff)
    if args.Report:
        _print_report(result.report)
    _emit_json_report(result.report, args.JsonReport)
    return _exit_code_for_report(result.report, options)


def _handle_batch(targets: list[str], args: argparse.Namespace) -> int:
    options = _options_from_args(args)
    report = convert_paths(targets, options=options)
    for change in report.file_changes:
        _print_file_change(change, show_diff=args.Diff)
    if args.Report:
        _print_report(report)
    _emit_json_report(report, args.JsonReport)
    return _exit_code_for_report(report, options)


def main() -> int:
    """CLI entrypoint."""

    parser = get_parser()
    try:
        args = parser.parse_args()
    except Exception:
        print("[WARNING] -m/--multiple flag expected at least one argument")
        return 1

    if args.Examples:
        print_examples()
        return 0

    if args.Help:
        parser.print_help()
        return 0

    targets: list[str] = []
    if args.Target is not None:
        targets.append(args.Target)
    if args.Multiple:
        targets.extend(args.Multiple)

    if not targets:
        parser.print_help()
        print("[WARNING] You must specify a target file or directory to convert.")
        return 1

    missing = [target for target in targets if not Path(target).exists()]
    for item in missing:
        print(f"[WARNING] Could not find path {item}")
    if missing and len(missing) == len(targets):
        return 1

    existing_targets = [target for target in targets if Path(target).exists()]
    if len(existing_targets) == 1 and Path(existing_targets[0]).is_file() and not args.Multiple:
        return _handle_single_file(Path(existing_targets[0]), args)

    if args.Output is not None:
        print("[WARNING] --outfile only applies to single-file conversion.")
    return _handle_batch(existing_targets, args)
