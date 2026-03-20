from __future__ import annotations

import subprocess
import sys

from tk_to_ctk import util


def test_has_listbox_detects_presence(tmp_path) -> None:
    source_path = tmp_path / "source.py"
    source_path.write_text("import tkinter as tk\nitems = tk.Listbox(root)\n", encoding="utf-8")
    other_path = tmp_path / "other.py"
    other_path.write_text("import tkinter as tk\nlabel = tk.Label(root)\n", encoding="utf-8")

    assert util.has_listbox(str(source_path)) is True
    assert util.has_listbox(str(other_path)) is False


def test_get_listbox_source_uses_packaged_template() -> None:
    source_lines = util.get_listbox_source()
    assert source_lines[0].startswith("class CTkListbox")


def test_importing_util_has_no_syntaxwarning() -> None:
    subprocess.run(
        [sys.executable, "-W", "error::SyntaxWarning", "-c", "import tk_to_ctk.util"],
        check=True,
    )
