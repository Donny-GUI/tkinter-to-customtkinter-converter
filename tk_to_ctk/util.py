"""Utility helpers retained for compatibility and tests."""

from __future__ import annotations

import ast
import copy
import platform

from .listbox_template import LISTBOX_TEMPLATE


def point(thing: object) -> object:
    """Return the same object reference."""

    return thing


def interface(thing: object) -> object:
    """Create a shallow copy."""

    return copy.copy(thing)


def clone(thing: object) -> object:
    """Create a deep copy."""

    return copy.deepcopy(thing)


def parsetree(source: str) -> ast.AST:
    """Parse source into an AST without swallowing parser behavior."""

    try:
        return ast.parse(source, type_comments=True)
    except SyntaxError:
        return ast.parse(source)


def get_operating_system() -> str:
    """Determine the current operating system."""

    system = platform.system()
    if system == "Windows":
        return "Windows"
    if system == "Linux":
        return "Linux"
    if system == "Darwin":
        return "macOS"
    return "Unknown"


pip_str = "pip" if get_operating_system() == "Windows" else "pip3"
python_str = "python" if get_operating_system() == "Windows" else "python3"


def classes_begin_index(lines: list[str]) -> int:
    """Find the insertion point for helper class definitions."""

    for index, line in enumerate(lines):
        if line.startswith("class "):
            return index

    for index, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            continue
        return index

    return len(lines)


def get_listbox_source() -> list[str]:
    """Return the packaged listbox helper as source lines."""

    return [f"{line}\n" for line in LISTBOX_TEMPLATE.splitlines()]


def has_listbox(filepath: str) -> bool:
    """Detect whether a file contains a tkinter Listbox constructor."""

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return "tk.Listbox(" in content or "Listbox(" in content


def print_warning(string: str) -> None:
    """Print a warning line."""

    print(f"[WARNING] {string}")


def print_update(string: str | list[str]) -> None:
    """Print an update line."""

    if isinstance(string, list):
        string = "[" + ", ".join(string) + "]"
    print(f"[UPDATE] {string}")
