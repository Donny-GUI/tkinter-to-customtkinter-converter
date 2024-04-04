import re


class WidgetReplacer:
    """
    A class to replace widgets in a script and add custom constants.

    Attributes:
        source (str): The path to the source script file.
        output (str): The path to the output script file.
        findables (dict): A dictionary containing findable patterns and their replacements.
        constants (list): A list of existing tkinter constants found in the script.
        used_constants (list): A list of constants used in the script.
    """

    tkinter_constants = [
        "ACTIVE",
        "ALL",
        "ANCHOR",
        "ARC",
        "BASELINE",
        "BEVEL",
        "BOTH",
        "BOTTOM",
        "BROWSE",
        "BUTT",
        "CASCADE",
        "CENTER",
        "CHAR",
        "CHECKBUTTON",
        "CHORD",
        "COMMAND",
        "DISABLED",
        "E",
        "END",
        "EW",
        "EXCEPTION",
        "EXTENDED",
        "FALSE",
        "FIRST",
        "FLAT",
        "GROOVE",
        "HIDDEN",
        "HORIZONTAL",
        "INSERT",
        "INSIDE",
        "LAST",
        "LEFT",
        "MITER",
        "MULTIPLE",
        "N",
        "NE",
        "NO",
        "NONE",
        "NORMAL",
        "NS",
        "NSEW",
        "NW",
        "OFF",
        "ON",
        "OUTSIDE",
        "PAGES",
        "PIESLICE",
        "PROJECTING",
        "RADIOBUTTON",
        "RAISED",
        "READABLE",
        "RIDGE",
        "RIGHT",
        "ROUND",
        "S",
        "SCROLL",
        "SE",
        "SEL",
        "SEL_FIRST",
        "SEL_LAST",
        "SEPARATOR",
        "SINGLE",
        "SOLID",
        "SUNKEN",
        "SW",
        "Synchronous",
        "SystemButton",
        "TOP",
        "TRUE",
        "UNITS",
        "VERTICAL",
        "W",
        "WORD",
        "WRITABLE",
        "X",
        "Y",
    ]

    def __init__(self, source: str, output: str) -> None:
        """
        Initialize the WidgetReplacer instance.

        Args:
            source (str): The path to the source script file.
            output (str): The path to the output script file.
        """
        self.source = source
        self.output = output
        self.findables = {}
        self.constants = []
        self.used_constants = []

    def add_findable(self, original: str, replacement: str) -> None:
        """
        Add a findable pattern and its replacement.

        Args:
            original (str): The original pattern to find.
            replacement (str): The replacement pattern.
        """
        self.findables[re.escape(original)] = replacement

    def replace_widgets(self):
        """
        Replace widgets in the script using findable patterns and replacements.
        """
        with open(self.source, "r", encoding="utf-8", errors="ignore") as f:
            script_content = f.read()
        out = ""
        for onst in self.tkinter_constants:
            if re.search(onst, script_content):
                self.constants.append(onst)

        for original, replacement in self.findables.items():
            pattern = r"\b{}\b".format(original)
            script_content = re.sub(pattern, replacement, script_content)

        with open(self.output, "w", errors="ignore") as f:
            f.write(script_content)

    def double_check(self):
        """
        Double-check and add custom tkinter constants to the script.
        """
        with open(self.output, "r") as f:
            script_content = f.readlines()

        out = "import customtkinter as ctk\nfrom customtkinter import "
        m = len(self.constants) - 1
        for index, constant in enumerate(self.constants):
            if index == m:
                out += f"{constant}"
            else:
                out += f"{constant}, "
        out += "\n"

        with open(self.output, "w") as f:
            f.write(out)
            for line in script_content:
                f.write(line)

    def add_constant(self, constant):
        """
        Add a custom constant to the list of constants.

        Args:
            constant (str): The constant to add.
        """
        self.constants.append(constant)
