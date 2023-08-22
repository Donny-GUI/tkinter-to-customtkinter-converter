import re
import os
import sys
import subprocess
try:
    from rich.status import Status
except:
    print(f"rich is not installed. Installing...")
    subprocess.run(["pip", "install", "rich"], check=True)
    print(f"rich has been installed.")
from rich.status import Status
from rich.console import Console


class WidgetReplacer:
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
    "Text",
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
    def __init__(self, source, output):
        self.source = source
        self.output = output
        self.findables = {}
        self.constants = []
        self.used_constants = []

    def add_findable(self, original, replacement):
        self.findables[re.escape(original)] = replacement

    def replace_widgets(self):
        with open(self.source, "r", encoding="utf-8", errors="ignore") as f:
            script_content = f.read()
        out= ""
        for onst in self.tkinter_constants:
            if re.search(onst, script_content):
                self.constants.append(onst)

        for original, replacement in self.findables.items():
            pattern = r'\b{}\b'.format(original)
            script_content = re.sub(pattern, replacement, script_content)

        with open(self.output, "w", errors="ignore") as f:
            f.write(script_content)


    def double_check(self):
        with open(self.output, "r") as f:
            script_content = f.readlines()

        out = "import customtkinter as ctk\nfrom customtkinter import "
        m = len(self.constants) -1
        for index, constant in enumerate(self.constants):
            if index == m:
                out+=f"{constant}"
            else:
                out+=f"{constant}, "
        out+="\n"

        with open(self.output, "w") as f:
            f.write(out)
            for line in script_content:
                f.write(line)

    def add_constant(self, constant):
        self.constants.append(constant)

def class_based(input, output):
# Define a list of standard Tkinter widget names and constants to replace

    tkinter_widgets = [
        "Button",
        "Canvas",
        "Checkbutton",
        "Entry",
        "Frame",
        "Label",
        "Menubutton",
        "Message",
        "Radiobutton",
        "Scale",
        "Scrollbar",
        "Text",
        "Toplevel",
    ]

    replacer = WidgetReplacer(input, output)
    for widget in tkinter_widgets:
        ctk_widget = f"ctk.CTk{widget}"
        replacer.add_findable(f"{widget}, ", f"")
        replacer.add_findable(f"{widget},", f"{ctk_widget},")
        replacer.add_findable(f" = {widget}(", f" = {ctk_widget}(")
        replacer.add_findable(f"={widget}(", f"={ctk_widget}(")
        replacer.add_findable(f": {widget} ", f": {ctk_widget} ")
        replacer.add_findable(f":{widget},", f":{ctk_widget},")
        replacer.add_findable(f":{widget}", f":{ctk_widget}")

    replacer.replace_widgets()
    replacer.double_check()

    exit()
import_options = [
    "import tkinter as tk",     # 0
    "import tkinter", # 1
    "from tkinter import *",    # 2
    "from tkinter import ",     # 3
    "import tkinter.constants", # 4
    "import tkinter.constants as tkc" # 5
]
import_outcome = [
    "import customtkinter as ctk",
    "import customtkinter",
    "from customtkinter import *",
    "from customtkinter import ",
    "import customtkinter.constants",
    "import customtkinter.constants as ctkc"
]
metaclass_list = [
    "(Tk):\n",
    "(tk.Tk):\n",
    "(tkinter.Tk):\n",
]
tkinter_widgets = [
    "Button", "Canvas", "Checkbutton", "Entry", "Frame", "Label",
     "Menubutton", "Message",  "Radiobutton",
    "Scale", "Scrollbar", "Text", "Toplevel",  "Treeview",
    "Frame", "Progressbar", "Separator"
]
ctk_widgets = ["CTk"+x for x in tkinter_widgets]
widget_placements = [
    "    {},\n", " = {}", ": {}", " : {}", "={}", "({}):" ,"{}, ", "{},"
]
def replacement(replace):
    return re.escape(replace)

def make_all_widget_placements():
    values = []
    for widget in tkinter_widgets:
        sublist = []
        for placement in widget_placements:
            sublist.append(replacement(placement.format(widget)))
        values.append(sublist)
    return values

def find_from_tkinter_imports(filename: str) -> list[str]:
    with open(filename, 'r', encoding="utf-8", errors="ignore") as rfile:
        lines = rfile.readlines()

    values = []
    for index, line in enumerate(lines):
        if line.startswith("from tkinter import "):
            start = len("from tkinter import ")
            value = line[start:]
            if "(" in value:
                subvalue = []
                sublines = iter(lines[index:])
                while True:
                    nextline = next(sublines).strip(" ")
                    if nextline.startswith(")"):
                        break
                    subvalue.append(nextline)
                for v in subvalue:
                    values.append(v)
            else:
                vals = value.split(",")
                for val in vals:
                    values.append(val.strip(" "))
    return values

def get_import_tkinter_as_tk(input_file:str) -> bool:
    lines = get_import_lines(input_file)
    for line in lines:
        if line.startswith("import tkinter as tk"):
            return True
    return False

def get_import_lines(filename:str)  -> list[str]:
    retv = []
    with open(filename, 'r') as f:
        content = f.readlines()
    for c in content:
        for item in ["from ", "import "]:
            if c.startswith(item):
                retv.append(c)
    return retv

def get_tkinter_import_types(filepath:str) -> None:
    with open(filepath, 'r') as f:
        content = f.readlines()
    for line in content:
        for option in import_options:
            if line.startswith(option):
                pass

def replace_bg_with_bg_color_in_file(file_path:str) -> None:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    cont = content.replace(", bg=", ", bg_color=").replace(", bg =", ", bg_color =")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)

def replace_fg_with_fg_color_in_file(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    cont = content.replace(", fg=", ", fg_color=").replace(", fg =", ", fg_color =")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)

def replace_meta_in_file(file_path:str) -> None:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    cont = content
    for index, widget in enumerate(tkinter_widgets):
        cont = cont.replace(f"({widget}):",f"(ctk.{ctk_widgets[index]}):")
    cont = cont.replace("(Tk):", "(ctk.CTk):")
    cont = cont.replace("Tk()", "ctk.CTk()")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)

def replace_config_with_configure(file_path:str) -> None:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    modified_content = re.sub(r'\.config\(', '.configure(', content)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(modified_content)


def find_errs(file_path:str):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        retv = []
        for line in lines:
            l = re.sub(r'ttk.\ctk\.', 'ctk.', line)
            retv.append(l)
    with open(file_path, "w", encoding="utf-8") as wfile:
        for l in retv:
            wfile.write(l)

def make_custom_tkinter(input_file:str, output_filename: str) -> None:
    with Status(f"Analyzing {input_file}...") as status:
        wr = WidgetReplacer(input_file, output_filename)
        for widget in tkinter_widgets:
            ctk_widget = f"ctk.CTk{widget}"
            wr.add_findable(f" {widget}(", f" {ctk_widget}(")
            wr.add_findable(f"  {widget}(", f"  {ctk_widget}(")
            wr.add_findable(f"{widget}(", f"{ctk_widget}(")
            wr.add_findable(f"{widget}, ", "")
            wr.add_findable(f"{widget},", f"{ctk_widget},")
            wr.add_findable(f" = {widget}(", f" = {ctk_widget}(")
            wr.add_findable(f"={widget}(", f"={ctk_widget}(")
            wr.add_findable(f": {widget} ", f": {ctk_widget} ")
            wr.add_findable(f":{widget},", f":{ctk_widget},")
            wr.add_findable(f":{widget}", f":{ctk_widget}")
        status.update("tk.Widget -> ctk.CTkWidget")
        for widg in tkinter_widgets:
            widget = "tk." + widg
            ctk_widget = f"ctk.CTk{widg}"
            wr.add_findable(f"{widget}(", f"{ctk_widget}(")
            wr.add_findable(f" {widget}(", f" {ctk_widget}(")
            wr.add_findable(f"  {widget}(", f"  {ctk_widget}(")
            wr.add_findable(f"{widget}, ", f"")
            wr.add_findable(f"{widget},", f"{ctk_widget},")
            wr.add_findable(f" = {widget}(", f" = {ctk_widget}(")
            wr.add_findable(f"={widget}(", f"={ctk_widget}(")
            wr.add_findable(f": {widget} ", f": {ctk_widget} ")
            wr.add_findable(f":{widget},", f":{ctk_widget},")
            wr.add_findable(f":{widget}", f":{ctk_widget}")
        status.update(" ttk.Widget -> ctk.CTkWidget" )
        for widg in tkinter_widgets:
            widget:str = "ttk." + widg
            ctk_widget:str = f"ctk.CTk{widg}"
            wr.add_findable("{0}(".format(widget), "{0}(".format(ctk_widget))
            wr.add_findable("{0}, ".format(widget), "")
            wr.add_findable(widget+",", "{0},".format(ctk_widget))
            wr.add_findable(" = {0}(".format(widget), " = {0}(".format(ctk_widget))
            wr.add_findable("={0}(".format(widget), "={0}(".format(ctk_widget))
            wr.add_findable(": {0} ".format(widget), ": {0} ".format(ctk_widget))
            wr.add_findable(":{0},".format(widget),  ":{0},".format(ctk_widget))
            wr.add_findable(":{0}".format(widget), ":{0}".format(ctk_widget))
        print("    Replacing all widgets...")
        wr.replace_widgets()
        print("    double checking constants...")
        wr.double_check()
        print("    finding .config/.configure...")
        replace_config_with_configure(file_path =output_filename)
        print("    finding bg/bg_color...")
        replace_bg_with_bg_color_in_file( file_path =output_filename)
        print("    finding fg/fg_color...")
        replace_fg_with_fg_color_in_file(file_path =output_filename)
        print("    finding meta class options...")
        replace_meta_in_file(file_path = output_filename)
        print("Success!")
        find_errs(file_path = output_filename)


if __name__ == "__main__":
    from rich.panel import Panel
    console = Console()
    if len(sys.argv) < 2:
        console.print(Panel(f"Tkinter to CustomTkinter \n\n  Usage:\n\t [dim]{__file__}[/dim]  [dim italic]target target[/dim italic]\n  Description:\n\t Convert your tkinter scripts to customtkinter scripts.", highlight="blue", title="v 1.1", title_align="left", width=80))

    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            output_file = "customtkinter_" + str(os.path.basename(os.path.splitext(sys.argv[1])[0])) + ".py"
            make_custom_tkinter(sys.argv[1], output_file)

        else:
            console.print(f"cant locate file {sys.argv[1]}")
    elif len(sys.argv) > 2:
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                output_file = "customtkinter_" + str(os.path.basename(os.path.splitext(arg)[0])) + ".py"
                make_custom_tkinter(arg, output_file)
            else:
                console.print(f"cant locate file {arg}")
