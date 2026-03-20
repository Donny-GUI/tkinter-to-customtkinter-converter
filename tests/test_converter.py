from __future__ import annotations

from pathlib import Path

from tk_to_ctk.converter import SourceConverter
from tk_to_ctk.models import ConversionOptions, RiskClass
from tk_to_ctk.service import convert_file, convert_source


def test_source_converter_rewrites_widgets_and_normalizes_imports() -> None:
    source = """
import tkinter as tk
from tkinter import ttk, HORIZONTAL

root = tk.Tk(bg="black")
label = ttk.Label(root, text="Hi", fg="white")
scale = tk.Scale(root, from_=0, to=10, resolution=1, orient=HORIZONTAL)
label.config(text="Bye", foreground="blue")
root.mainloop()
""".strip()

    converted = SourceConverter().from_string(source)

    assert converted.count("import customtkinter as ctk") == 1
    assert 'root = ctk.CTk(fg_color="black")' in converted
    assert 'label = ctk.CTkLabel(root, text="Hi", text_color="white")' in converted
    assert "scale = ctk.CTkSlider(" in converted
    assert "orientation=tk.HORIZONTAL" in converted
    assert "number_of_steps = 10" in converted
    assert 'label.configure(text="Bye", text_color="blue")' in converted
    assert "TODO tk2ctk" not in converted


def test_direct_imports_and_base_classes_are_rewritten() -> None:
    source = """
from tkinter import Tk, Label, StringVar, HORIZONTAL

class App(Tk):
    pass

value = StringVar()
label = Label(App(), fg="white")
angle = HORIZONTAL
""".strip()

    converted = convert_source(source)

    assert "class App(ctk.CTk):" in converted.source
    assert "value = tk.StringVar()" in converted.source
    assert 'label = ctk.CTkLabel(App(), text_color="white")' in converted.source
    assert "angle = tk.HORIZONTAL" in converted.source
    assert converted.source.count("import customtkinter as ctk") == 1
    assert converted.source.count("import tkinter as tk") == 1


def test_unsupported_widgets_are_preserved_with_diagnostics() -> None:
    source = """
import tkinter as tk

root = tk.Tk()
menu = tk.Menu(root)
""".strip()

    result = convert_source(source)

    assert "# TODO tk2ctk: CustomTkinter has no direct Menu replacement." in result.source
    assert "menu = tk.Menu(root)" in result.source
    assert any("Menu replacement" in diagnostic.message for diagnostic in result.diagnostics)


def test_option_menu_and_progressbar_special_cases_are_handled() -> None:
    source = """
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
selected = tk.StringVar(value="One")
menu = tk.OptionMenu(root, selected, "One", "Two", "Three")
progress = ttk.Progressbar(root, value=30, maximum=60)
""".strip()

    result = convert_source(source)

    assert "menu = ctk.CTkOptionMenu(root" in result.source
    assert 'variable = selected' in result.source
    assert 'values = ["One", "Two", "Three"]' in result.source
    assert 'menu.set("One")' in result.source
    assert "progress = ctk.CTkProgressBar(root)" in result.source
    assert "progress.set(0.5)" in result.source


def test_listbox_conversion_is_gated_by_option() -> None:
    source = """
import tkinter as tk

items = tk.Listbox(root)
""".strip()

    preserved = convert_source(source)
    converted = convert_source(source, ConversionOptions(convert_listboxes=True))

    assert "items = tk.Listbox(root)" in preserved.source
    assert "TODO tk2ctk: Preserved tk.Listbox." in preserved.source
    assert "class CTkListbox" in converted.source
    assert "items = CTkListbox(root)" in converted.source


def test_dynamic_widget_references_are_converted() -> None:
    source = """
import tkinter as tk

widgets = [tk.Button, tk.Label]
ButtonClass = tk.Button
root = tk.Tk()
created = [factory(root) for factory in widgets]
btn = ButtonClass(root)
""".strip()

    result = convert_source(source)

    assert "widgets = [ctk.CTkButton, ctk.CTkLabel]" in result.source
    assert "ButtonClass = ctk.CTkButton" in result.source
    assert "root = ctk.CTk()" in result.source


def test_reconversion_is_idempotent_for_unsupported_widgets() -> None:
    source = """
import tkinter as tk

root = tk.Tk()
menu = tk.Menu(root)
""".strip()

    first = convert_source(source)
    second = convert_source(first.source)

    assert first.source == second.source
    assert first.source.count("TODO tk2ctk: CustomTkinter has no direct Menu replacement.") == 1


def test_report_tracks_converted_and_unchanged_widgets() -> None:
    source = """
import tkinter as tk

widgets = [tk.Button, tk.Label]
root = tk.Tk()
menu = tk.Menu(root)
""".strip()

    result = convert_source(source, ConversionOptions(report=True))

    assert result.report.widgets_converted >= 3
    assert result.report.widgets_left_unchanged == 1
    assert result.report.unsupported_widgets == {"tk.Menu": 1}
    assert result.report.warnings_emitted == 1
    assert result.risk_class == RiskClass.REVIEW
    assert result.should_review is True


def test_wildcard_imports_are_preserved_with_warning() -> None:
    source = """
from tkinter import *

root = Tk()
label = Label(root, text="Hi")
""".strip()

    result = convert_source(source)

    assert "from tkinter import *" in result.source
    assert "TODO tk2ctk: Preserved 'from tkinter import *'. Wildcard imports are not normalized safely." in result.source
    assert len(result.diagnostics) == 1


def test_multiline_fixture_preserves_comments_and_expected_output() -> None:
    source = Path("tests/fixtures/realistic_app_input.py").read_text(encoding="utf-8")
    expected = Path("tests/fixtures/realistic_app_expected.py").read_text(encoding="utf-8")

    result = convert_source(source)

    assert result.source == expected
    assert "# Top-level helper comment should survive conversion." in result.source
    assert "# Builder comments should remain readable." in result.source
    assert "super().__init__(master, fg_color=\"white\")" in result.source
    assert "CustomTkinter has no direct Canvas replacement." in result.source


def test_parse_failure_is_reported_without_changing_source() -> None:
    source = "import tkinter as tk\nroot = tk.Tk(\n"

    result = convert_source(source)

    assert result.success is False
    assert result.source == source
    assert result.diagnostics[0].category == "parse_error"
    assert result.risk_class == RiskClass.UNSAFE


def test_convert_file_dry_run_does_not_write_output(tmp_path) -> None:
    input_path = tmp_path / "input.py"
    output_path = tmp_path / "out.py"
    input_path.write_text("import tkinter as tk\nroot = tk.Tk()\n", encoding="utf-8")

    result = convert_file(input_path, output_path, ConversionOptions(dry_run=True))

    assert result.success is True
    assert result.changed is True
    assert not output_path.exists()
    assert result.report.file_changes[0].reason == "dry_run"


def test_safe_classification_for_warning_free_file() -> None:
    source = "import tkinter as tk\nroot = tk.Tk()\nlabel = tk.Label(root, text='Hi')\n"

    result = convert_source(source, ConversionOptions(report=True))

    assert result.success is True
    assert result.risk_class == RiskClass.SAFE
    assert result.should_review is False
    assert result.report.files_by_risk == {"safe": 1}


def test_review_classification_when_warnings_are_within_threshold() -> None:
    source = "import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\n"

    result = convert_source(source, ConversionOptions(report=True, max_warnings=5, max_unsupported=5))

    assert result.success is True
    assert result.risk_class == RiskClass.REVIEW
    assert result.report.diagnostics_by_severity["warning"] == 1
    assert result.report.unsupported_widget_count == 1


def test_unsafe_classification_when_warning_threshold_is_exceeded() -> None:
    source = """
import tkinter as tk

root = tk.Tk()
menu = tk.Menu(root)
canvas = tk.Canvas(root)
message = tk.Message(root)
""".strip()

    result = convert_source(source, ConversionOptions(report=True, max_warnings=1, max_unsupported=10))

    assert result.success is True
    assert result.risk_class == RiskClass.UNSAFE
    assert result.should_review is True


def test_unsafe_classification_when_unsupported_threshold_is_exceeded() -> None:
    source = """
import tkinter as tk

root = tk.Tk()
menu = tk.Menu(root)
canvas = tk.Canvas(root)
""".strip()

    result = convert_source(source, ConversionOptions(report=True, max_warnings=10, max_unsupported=1))

    assert result.success is True
    assert result.risk_class == RiskClass.UNSAFE


def test_in_place_write_is_blocked_for_unsafe_files_by_default(tmp_path) -> None:
    input_path = tmp_path / "input.py"
    original = "import tkinter as tk\nroot = tk.Tk()\nmenu = tk.Menu(root)\ncanvas = tk.Canvas(root)\n"
    input_path.write_text(original, encoding="utf-8")

    result = convert_file(
        input_path,
        input_path,
        ConversionOptions(write_in_place=True, max_warnings=1, max_unsupported=1),
    )

    assert result.success is True
    assert result.risk_class == RiskClass.UNSAFE
    assert result.report.file_changes[0].reason == "unsafe_write_blocked"
    assert input_path.read_text(encoding="utf-8") == original


def test_safe_repeated_conversion_marks_already_converted_file_unchanged(tmp_path) -> None:
    input_path = tmp_path / "input.py"
    input_path.write_text(
        "import customtkinter as ctk\nroot = ctk.CTk()\nlabel = ctk.CTkLabel(root, text='Hi')\n",
        encoding="utf-8",
    )

    result = convert_file(input_path, input_path, ConversionOptions(write_in_place=True))

    assert result.success is True
    assert result.changed is False
    assert result.skipped is True


def test_in_place_backup_writes_backup_file(tmp_path) -> None:
    input_path = tmp_path / "input.py"
    original = "import tkinter as tk\nroot = tk.Tk()\n"
    input_path.write_text(original, encoding="utf-8")

    result = convert_file(
        input_path,
        input_path,
        ConversionOptions(write_in_place=True, backup=True),
    )

    assert result.success is True
    assert input_path.with_suffix(".py.bak").exists()
    assert input_path.with_suffix(".py.bak").read_text(encoding="utf-8") == original


def test_real_repo_gui_file_converts_cleanly() -> None:
    source = Path("tk_to_ctk/test.py").read_text(encoding="utf-8")

    result = convert_source(source, ConversionOptions(report=True))

    assert result.success is True
    assert result.report.warnings_emitted == 0
    assert "root = ctk.CTk()" in result.source
    assert "button_frame = ctk.CTkFrame(root)" in result.source
    assert "search_button = ctk.CTkButton(" in result.source
    assert "text_box = ctk.CTkTextbox(" in result.source
    assert "tk.filedialog.askopenfilename" in result.source


def test_large_mixed_repo_sample_does_not_crash_and_keeps_warning_locations() -> None:
    source = Path("tests/fixtures/customtkinter_test_input.py").read_text(encoding="utf-8")

    result = convert_source(source, ConversionOptions(report=True, convert_listboxes=True))

    assert result.success is True
    assert not any(d.level == "error" for d in result.diagnostics)
    assert result.report.warnings_emitted > 0
    assert all(
        diagnostic.line is not None
        for diagnostic in result.diagnostics
        if diagnostic.level == "warning"
    )
