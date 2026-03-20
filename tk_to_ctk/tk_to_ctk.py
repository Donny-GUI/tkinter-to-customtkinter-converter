"""Legacy-compatible public entrypoints for the converter."""

from __future__ import annotations

import os
from pathlib import Path

from .cli import main
from .models import ConversionOptions
from .service import convert_file


def input_filename_to_output_filename(input_filename: str) -> str:
    """Match the historic default output naming convention."""

    return os.path.join(
        os.getcwd(),
        "customtkinter_" + os.path.basename(str(input_filename)),
    )


def make_custom_tkinter(
    input_file: str,
    output_filename: str,
    convert_listboxes: bool = False,
    verbose: bool = False,
) -> None:
    """Compatibility wrapper for the legacy file conversion API."""

    options = ConversionOptions(
        convert_listboxes=convert_listboxes,
        verbose=verbose,
    )
    convert_file(Path(input_file), Path(output_filename), options=options)
