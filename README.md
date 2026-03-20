# Tkinter to CustomTkinter Converter

`tkinter-to-customtkinter-converter` is a beta migration assistant for converting reviewable `tkinter` source files into `customtkinter` code.

It is designed for real project migrations, not blind search-and-replace:

- supported patterns are rewritten structurally with LibCST
- unsupported or ambiguous patterns are preserved with diagnostics and `# TODO tk2ctk:` comments
- files are classified as `safe`, `review`, or `unsafe` so you can decide what to apply automatically

This is still a beta tool. It should be used to accelerate migration, not to remove code review.

## What It Does

- converts supported `tkinter` and `ttk` widget construction patterns to `customtkinter`
- rewrites imports, subclass bases, and supported `.config()` calls
- preserves comments and source structure as much as practical
- emits human-readable and JSON reports for file-level and project-level review
- supports preview, diff, dry-run, output directory, recursive traversal, backups, and batch processing

## What It Does Not Do

- it does not promise a full semantic port of every `tkinter` app
- it does not invent replacements for unsupported widgets
- it does not reliably resolve heavily dynamic runtime behavior
- it does not make styling, theme, or layout decisions beyond safe structural rewrites
- it does not guarantee that a converted file is ready to run without review

## Install

Python 3.11+ is required.

Install the beta from a checkout:

```bash
git clone https://github.com/Donny-GUI/tkinter-to-customtkinter-converter.git
cd tkinter-to-customtkinter-converter
python -m pip install .
```

Install with test dependencies for local development:

```bash
python -m pip install -e .[dev]
```

Verify the CLI is available:

```bash
tk2ctk --version
```

## CLI Quickstart

Preview a single file:

```bash
tk2ctk app.py --dry-run --diff --report
```

Convert a single file to a separate output:

```bash
tk2ctk app.py -o converted_app.py
```

Convert a project tree into a parallel directory:

```bash
tk2ctk src --recursive --output-dir converted_src --report --json-report report.json
```

Apply safe in-place conversion with backups:

```bash
tk2ctk src --recursive --in-place --backup --only-safe --report
```

Fail CI if any file is classified as `unsafe`:

```bash
tk2ctk src --recursive --dry-run --report --fail-on-unsafe
```

## Preview and Diff Workflow

Recommended first pass:

```bash
tk2ctk src --recursive --dry-run --diff --report --json-report report.json
```

That gives you:

- unified diffs without writing files
- warnings with file and line locations
- per-file `safe` / `review` / `unsafe` classification
- machine-readable output for batch inspection

## Safety Classes

Each processed file is classified as:

- `safe`: converted with no warnings or only non-impacting informational notes
- `review`: converted, but emitted warnings or preserved unsupported constructs within configured thresholds
- `unsafe`: parse/transform failure, or warning volume above threshold, or unsupported-widget volume above threshold

Useful CLI controls:

- `--max-warnings N`
- `--max-unsupported N`
- `--fail-on-unsafe`
- `--fail-on-review`
- `--only-safe`
- `--only-review`
- `--only-unsafe`
- `--allow-unsafe-write`

Default behavior is conservative:

- preview and reporting are available for all files
- in-place writes are blocked for `unsafe` files unless `--allow-unsafe-write` is set

## Supported Widgets

These are converted when the source pattern is statically recognizable:

- `tk.Tk` -> `ctk.CTk`
- `tk.Toplevel` -> `ctk.CTkToplevel`
- `tk.Frame`, `ttk.Frame` -> `ctk.CTkFrame`
- `tk.Label`, `ttk.Label` -> `ctk.CTkLabel`
- `tk.Button`, `ttk.Button` -> `ctk.CTkButton`
- `tk.Entry`, `ttk.Entry` -> `ctk.CTkEntry`
- `tk.Checkbutton`, `ttk.Checkbutton` -> `ctk.CTkCheckBox`
- `tk.Radiobutton`, `ttk.Radiobutton` -> `ctk.CTkRadioButton`
- `tk.Scrollbar`, `ttk.Scrollbar` -> `ctk.CTkScrollbar`
- `tk.Text` -> `ctk.CTkTextbox`
- `ttk.Combobox` -> `ctk.CTkComboBox`
- `tk.Scale`, `ttk.Scale` -> `ctk.CTkSlider`
- `tk.OptionMenu` -> `ctk.CTkOptionMenu` for the standard positional signature
- `ttk.Progressbar` -> `ctk.CTkProgressBar` when normalization can be computed safely
- `tk.Listbox` -> preserved by default, or converted using an inline `CTkListbox` shim with `--listboxes`

Other supported patterns:

- `import tkinter as tk`
- `from tkinter import ...`
- mixed `tkinter` and `ttk` imports
- subclass bases like `class App(tk.Tk)`
- `.config(...)` to `.configure(...)` on converted widgets
- simple dynamic widget references such as `widgets = [tk.Button, tk.Label]`

## Preserved With Warnings

These are not claimed as converted. They remain `tkinter` or `ttk` code with explicit diagnostics:

- `tk.Menu`
- `tk.Menubutton`
- `tk.Canvas`
- `tk.Message`
- `tk.PanedWindow`
- `tk.LabelFrame`
- `ttk.Treeview`
- `ttk.Separator`
- `ttk.Notebook`
- `ttk.Panedwindow`
- `ttk.Labelframe`
- wildcard imports such as `from tkinter import *`
- ambiguous `OptionMenu` signatures
- `Progressbar` patterns that depend on runtime state
- `Scale.resolution` values that cannot be mapped safely

## JSON Report Usage

Write a machine-readable report:

```bash
tk2ctk src --recursive --dry-run --json-report report.json
```

Write the JSON report to stdout:

```bash
tk2ctk app.py --dry-run --json-report -
```

Reports include:

- file risk class
- warning counts by severity
- unsupported widget counts
- widgets converted by type
- unsupported widgets by type
- warnings by category
- files scanned, changed, skipped, and failed

## Recommended Migration Workflow

1. Run `tk2ctk src --recursive --dry-run --diff --report --json-report report.json`.
2. Review `unsafe` files first. Do not batch-apply them blindly.
3. Review `review` files for preserved widgets, dropped options, and TODO comments.
4. Convert `safe` files into an output directory with `--only-safe --output-dir converted_src`.
5. For files you are comfortable applying directly, use `--in-place --backup`.
6. Run your project tests and manually verify the UI.

## Command Reference

```text
tk2ctk [TARGET] [options]
```

Key options:

- `--version`
- `-o, --outfile`
- `--output-dir DIR`
- `--in-place`
- `--recursive`
- `--include GLOB`
- `--exclude GLOB`
- `--dry-run`
- `--diff`
- `--backup`
- `--listboxes`
- `--report`
- `--json-report [PATH]`
- `--max-warnings N`
- `--max-unsupported N`
- `--fail-on-unsafe`
- `--fail-on-review`
- `--only-safe`
- `--only-review`
- `--only-unsafe`
- `--allow-unsafe-write`

## Python API

```python
from tk_to_ctk.converter import SourceConverter

converter = SourceConverter(convert_listboxes=False)
converted = converter.from_string(source_text)
```

Lower-level service API:

```python
from tk_to_ctk.models import ConversionOptions
from tk_to_ctk.service import convert_source, convert_file, convert_paths

result = convert_source(source_text, ConversionOptions(report=True))
file_result = convert_file("input.py", "output.py")
project_report = convert_paths(
    ["src"],
    ConversionOptions(recursive=True, output_dir="converted_src", report=True),
)
```

## Beta Caveats

Be explicit about these limits when using the tool:

- unsupported widgets are preserved, not solved
- wildcard imports remain intentionally conservative
- dynamic aliasing, `exec`, string-built code, and complex runtime widget factories are outside reliable static analysis
- `safe` means low-risk structurally, not “no human review needed”
- files with heavy mixed `tkinter` and already-converted `customtkinter` code can still produce noisy but correct warnings

This project is ready for beta usage as a migration assistant, but the output should still be reviewed before shipping.
