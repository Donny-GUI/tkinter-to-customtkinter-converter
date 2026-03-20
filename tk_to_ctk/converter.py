"""Compatibility facade for source-to-source conversion."""

from __future__ import annotations

from pathlib import Path

from .models import ConversionOptions
from .service import convert_source


class SourceConverter:
    """Convert tkinter source strings or files into customtkinter source."""

    def __init__(self, *, convert_listboxes: bool = False, verbose: bool = False) -> None:
        self.options = ConversionOptions(
            convert_listboxes=convert_listboxes,
            verbose=verbose,
        )

    def from_string(self, string: str) -> str:
        """Convert raw source text."""

        return convert_source(string, self.options).source

    def from_file(self, filepath: str) -> str:
        """Read a file and convert its contents."""

        return self.from_string(Path(filepath).read_text(encoding="utf-8"))
