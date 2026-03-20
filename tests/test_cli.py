from __future__ import annotations

import json
from pathlib import Path

from tk_to_ctk import __version__
from tk_to_ctk import cli


def test_cli_single_file_conversion(tmp_path, monkeypatch, capsys) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    input_path.write_text(
        'import tkinter as tk\nroot = tk.Tk()\nlabel = tk.Label(root, fg="white")\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(input_path), "-o", str(output_path)],
    )

    cli.main()
    captured = capsys.readouterr()

    assert output_path.exists()
    converted = output_path.read_text(encoding="utf-8")
    assert "ctk.CTk()" in converted
    assert "ctk.CTkLabel" in converted
    assert "[CHANGED]" in captured.out


def test_cli_report_mode_outputs_summary(tmp_path, monkeypatch, capsys) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    input_path.write_text(
        "import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(input_path), "-o", str(output_path), "--report"],
    )

    cli.main()
    captured = capsys.readouterr()

    assert "widgets converted:" in captured.out
    assert "widgets left unchanged:" in captured.out
    assert "unsupported widgets:" in captured.out
    assert "files processed:" in captured.out


def test_cli_directory_mode_with_output_dir(tmp_path, monkeypatch, capsys) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")
    out = tmp_path / "converted"

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(src), "--output-dir", str(out)],
    )

    exit_code = cli.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert (out / "app.py").exists()
    assert "[CHANGED]" in captured.out


def test_cli_recursive_include_exclude_filters(tmp_path, monkeypatch) -> None:
    src = tmp_path / "src"
    pkg = src / "pkg"
    skip = src / "skip"
    pkg.mkdir(parents=True)
    skip.mkdir(parents=True)
    (pkg / "include_me.py").write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")
    (skip / "ignore_me.py").write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")
    out = tmp_path / "converted"

    monkeypatch.setattr(
        "sys.argv",
        [
            "tk2ctk",
            str(src),
            "--recursive",
            "--include",
            "pkg/*.py",
            "--exclude",
            "skip/*.py",
            "--output-dir",
            str(out),
        ],
    )

    exit_code = cli.main()

    assert exit_code == 0
    assert (out / "pkg" / "include_me.py").exists()
    assert not (out / "skip" / "ignore_me.py").exists()


def test_cli_dry_run_and_diff_do_not_write_files(tmp_path, monkeypatch, capsys) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    input_path.write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(input_path), "-o", str(output_path), "--dry-run", "--diff"],
    )

    exit_code = cli.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert not output_path.exists()
    assert "--- " in captured.out
    assert "+++ " in captured.out


def test_cli_json_report_mode_writes_machine_readable_report(tmp_path, monkeypatch) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    report_path = tmp_path / "report.json"
    input_path.write_text("import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(input_path), "-o", str(output_path), "--json-report", str(report_path)],
    )

    exit_code = cli.main()

    assert exit_code == 0
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["files_processed"] == 1
    assert payload["unsupported_widgets"]["tk.Menu"] == 1
    assert payload["file_changes"][0]["input_path"] == str(input_path)


def test_cli_parse_failure_returns_nonzero_exit_code(tmp_path, monkeypatch, capsys) -> None:
    input_path = tmp_path / "broken.py"
    output_path = tmp_path / "output.py"
    input_path.write_text("import tkinter as tk\nroot = tk.Tk(\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["tk2ctk", str(input_path), "-o", str(output_path)],
    )

    exit_code = cli.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert not output_path.exists()
    assert "parse_error" in captured.out


def test_cli_version_flag_prints_package_version(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["tk2ctk", "--version"])

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 0

    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_cli_fail_on_unsafe_returns_nonzero_for_unsafe_file(tmp_path, monkeypatch) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    input_path.write_text(
        "import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\ncanvas = tk.Canvas(root)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tk2ctk",
            str(input_path),
            "-o",
            str(output_path),
            "--max-warnings",
            "1",
            "--fail-on-unsafe",
        ],
    )

    exit_code = cli.main()

    assert exit_code == 1


def test_cli_fail_on_review_returns_nonzero_for_review_file(tmp_path, monkeypatch) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "output.py"
    input_path.write_text(
        "import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tk2ctk",
            str(input_path),
            "-o",
            str(output_path),
            "--fail-on-review",
        ],
    )

    exit_code = cli.main()

    assert exit_code == 1


def test_cli_only_safe_filters_out_review_writes(tmp_path, monkeypatch) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "safe.py").write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")
    (src / "review.py").write_text("import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\n", encoding="utf-8")
    out = tmp_path / "converted"

    monkeypatch.setattr(
        "sys.argv",
        [
            "tk2ctk",
            str(src),
            "--output-dir",
            str(out),
            "--only-safe",
        ],
    )

    exit_code = cli.main()

    assert exit_code == 0
    assert (out / "safe.py").exists()
    assert not (out / "review.py").exists()
