"""Public package surface for tkinter-to-customtkinter conversion."""

from ._version import __version__
from .cli import main
from .converter import SourceConverter
from .tk_to_ctk import input_filename_to_output_filename, make_custom_tkinter

__all__ = [
    "SourceConverter",
    "__version__",
    "input_filename_to_output_filename",
    "main",
    "make_custom_tkinter",
]
