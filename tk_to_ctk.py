import os
import dataclasses
import re
import sys
import tkinter as tk
from tkinter import filedialog


# ======================================================================
# User:       Donny-GUI
# Author:     Donald Guiles
# Date:       March 13 2023
#  
# Description:
#       Converts a tkinter python3 script into a python3 customtkinter
#       script. Determines the programming paradigm and import type
#       and converts the script into a customtkinter script with the
#       programming paradigm and import type originally specified.
#
# License:    MIT License
#   Free to use and distribute under the MIT License for any purpose.  
#   Give credit where credit is due. If not, you'll be cursed with
#   the ghost of java programming for 100 years.
#
#   CustomTkinter was created by TomSchimansky:
#   https://github.com/TomSchimansky/CustomTkinter
#
#
# ======================================================================

# ======================================================================
# Updates Log
#
# [4/14/2023]  -  ttk is now supported by default
#       new data class - TtkRegex
#       new data class - TtkChanger
#       new function   - class_based_ttk
#       new function   - function_based_ttk
#       new function   - determine_if_program_uses_ttk
#       new data class - MiscellaneousRegex
#       new function   - ttk_prescan
#
# [4/14/2023]  -  General syntax Fixes
#       filename parse - integrated os.sep into filename determination.
#       path parse     - integrated os.sep into path determination.
#
# ======================================================================


@dataclasses.dataclass(slots=True)
class Change:
    import_statement = ("import tkinter as tk", "import customtkinter as ctk")
    tk = ("tk.Tk()", "ctk.CTk()")
    tk3 = ("Tk", "CTk")
    tk2 = ("tk.Tk, ctk.CTk")
    label = ("tk.Label", "ctk.CTkLabel")
    button = ("tk.Button", "ctk.CTkButton")
    entry = ("tk.Entry", "ctk.CTkEntry")
    combo = ("tk.Combobox", "ctk.CTkCombobox")
    textbox = ("tk.Textbox", "ctk.CTkTextbox")
    progressbar = ("tk.Progressbar", "ctk.CTkProgressbar")
    frame = ("tk.Frame", "ctk.CTkFrame")
    option_menu = ("tk.OptionMenu", "ctk.CTkOptionMenu")
    radiobutton = ("tk.Radiobutton", "ctk.CTkRadioButton")
    segemented_button = ("tk.SegmentedButton", "ctk.CTkSegmentedButton")
    checkbox = ("tk.CheckBox", "ctk.CTkCheckBox")
    input_dialog = ("tk.InputDialog", "ctk.CTkInputDialog")
    slider = ("tk.Slider", "ctk.CTkSlider")
    switch = ("tk.Switch", "ctk.CTkSwitch")
    image = ("tk.Image", "ctk.CTkImage")
    toplevel = ("tk.Toplevel", "ctk.CTkTopLevel")
    regex_config = (".config", ".configure")
    background_color_fix_1 = (", background_color=", "bg_color=")
    foreground_color_fix_1 = (", foreground_color=", "fg_color=")
    background_color_fix_2 = (", background_color = ", "bg_color = ")
    foreground_color_fix_2 = (", foreground_color = ", "fg_color = ")
    all = [import_statement, tk, tk2, label, button, entry, combo, textbox, progressbar, frame, option_menu, radiobutton, switch, image, slider, regex_config, background_color_fix_1, background_color_fix_2, foreground_color_fix_1, foreground_color_fix_2]
    tks = [x[0] for x in all]
    ctks = [x[1] for x in all]


@dataclasses.dataclass(slots=True)
class Change2:
    import_statement = ("from tkinter import *", "from customtkinter import *")
    label = ("Label", "CTkLabel")
    button = ("Button", "CTkButton")
    entry = ("Entry", "CTkEntry")
    combo = ("Combobox", "CTkComboBox")
    textbox = ("Textbox", "CTkTextBox")
    progressbar = ("Progressbar", "CTkProgressBar")
    frame = ("Frame", "CTkFrame")
    option_menu = ("OptionMenu", "CTkOptionMenu")
    radiobutton = ("Radiobutton", "CTkRadioButton")
    segemented_button = ("SegmentedButton", "CTkSegmentedButton")
    checkbox = ("CheckBox", "CTkCheckBox")
    input_dialog = ("InputDialog", "CTkInputDialog")
    slider = ("Slider", "CTkSlider")
    switch = ("Switch", "CTkSwitch")
    image = ("Image", "CTkImage")
    toplevel = ("Toplevel", "CTkTopLevel")
    regex_config = (".config", ".configure")
    background_color_fix_1 = (", background_color=", "bg_color=")
    foreground_color_fix_1 = (", foreground_color=", "fg_color=")
    background_color_fix_2 = (", background_color = ", "bg_color = ")
    foreground_color_fix_2 = (", foreground_color = ", "fg_color = ")
    all = [import_statement, label, button, entry, combo, textbox, progressbar, frame, option_menu, radiobutton, switch, image, slider, regex_config, background_color_fix_1, background_color_fix_2, foreground_color_fix_1, foreground_color_fix_2]
    tks = [x[0] for x in all]
    ctks = [x[1] for x in all]


@dataclasses.dataclass(slots=True)
class Type2Regex:
    difference = 3
    button = re.compile(r'\b Button\b')
    canvas = re.compile(r'\bCanvas\b')
    combo       = re.compile(r'\bCombobox\b')
    checkbutton = re.compile(r'\bCheckbutton\b')
    entry       = re.compile(r'\bEntry\b')
    frame       = re.compile(r'\bFrame\b')
    label       = re.compile(r'\bLabel\b')
    listbox     = re.compile(r'\bListbox\b')
    menu        = re.compile(r'\bMenu\b')
    menubutton  = re.compile(r'\bMenubutton\b')
    message     = re.compile(r'\bMessage\b')
    optionmenu  = re.compile(r'\bOptionMenu\b')
    panedwindow = re.compile(r'\bPanedWindow\b')
    radiobutton = re.compile(r'\bRadiobutton\b')
    scale       = re.compile(r'\bScale\b')
    scrollbar   = re.compile(r'\bScrollbar\b')
    text        = re.compile(r'\bText\b')
    toplevel    = re.compile(r'\bToplevel\b')
    spinbox     = re.compile(r'\bSpinbox\b')
    labelframe  = re.compile(r'\bLabelFrame\b')
    image       = re.compile(r'\bImage\b')
    all = [button, canvas, checkbutton, entry, frame, label, listbox, menu, menubutton, message, optionmenu, panedwindow, radiobutton, scale, text, toplevel, spinbox, labelframe]


@dataclasses.dataclass(slots=True)
class Type1Regex:
    difference = 5
    button      = re.compile(r'\btk.Button\b')
    canvas      = re.compile(r'\btk.Canvas\b')
    combo       = re.compile(r'\btk.Combobox\b')
    checkbutton = re.compile(r'\btk.Checkbutton\b')
    entry       = re.compile(r'\btk.Entry\b')
    frame       = re.compile(r'\btk.Frame\b')
    label       = re.compile(r'\btk.Label\b')
    listbox     = re.compile(r'\btk.Listbox\b')
    menu        = re.compile(r'\btk.Menu\b')
    menubutton  = re.compile(r'\btk.Menubutton\b')
    message     = re.compile(r'\btk.Message\b')
    optionmenu  = re.compile(r'\btk.OptionMenu\b')
    panedwindow = re.compile(r'\btk.PanedWindow\b')
    radiobutton = re.compile(r'\btk.Radiobutton\b')
    scale       = re.compile(r'\btk.Scale\b')
    scrollbar   = re.compile(r'\btk.Scrollbar\b')
    text        = re.compile(r'\btk.Text\b')
    toplevel    = re.compile(r'\btk.Toplevel\b')
    spinbox     = re.compile(r'\btk.Spinbox\b')
    labelframe  = re.compile(r'\btk.LabelFrame\b')
    image       = re.compile(r'\btk.Image\b')
    all = [button, canvas, checkbutton, entry, frame, label, listbox, menu, menubutton, message, optionmenu, panedwindow, radiobutton, scale, text, toplevel, spinbox, labelframe]


@dataclasses.dataclass(slots=True)
class TtkRegex:
    import_statement_1 = re.compile(r"\bfrom tkinter import ttk\b")
    package     = re.compile(r"ttk.")
    button      = re.compile(r'\bttk.Button\b')
    canvas      = re.compile(r'\bttk.Canvas\b')
    combo       = re.compile(r'\bttk.Combobox\b')
    checkbutton = re.compile(r'\bttk.Checkbutton\b')
    entry       = re.compile(r'\bttk.Entry\b')
    frame       = re.compile(r'\bttk.Frame\b')
    label       = re.compile(r'\bttk.Label\b')
    listbox     = re.compile(r'\bttk.Listbox\b')
    menu        = re.compile(r'\bttk.Menu\b')
    menubutton  = re.compile(r'\bttk.Menubutton\b')
    message     = re.compile(r'\bttk.Message\b')
    optionmenu  = re.compile(r'\bttk.OptionMenu\b')
    panedwindow = re.compile(r'\bttk.PanedWindow\b')
    radiobutton = re.compile(r'\bttk.Radiobutton\b')
    scale       = re.compile(r'\bttk.Scale\b')
    scrollbar   = re.compile(r'\bttk.Scrollbar\b')
    text        = re.compile(r'\bttk.Text\b')
    toplevel    = re.compile(r'\bttk.Toplevel\b')
    spinbox     = re.compile(r'\bttk.Spinbox\b')
    labelframe  = re.compile(r'\bttk.LabelFrame\b')
    image       = re.compile(r'\bttk.Image\b')
    all = [button, canvas, checkbutton, entry, frame, label, listbox, menu, menubutton, message, optionmenu, panedwindow, radiobutton, scale, text, toplevel, spinbox, labelframe]


@dataclasses.dataclass(slots=True)
class TtkChanger:
    import_statement = ("from tkinter import ttk", "import customtkinter as ctk")
    ttk = ("ttk.Tk()", "ctk.CTk()")
    ttk2 = ("ttk.Tk, ctk.CTk")
    label = ("ttk.Label", "ctk.CTkLabel")
    button = ("ttk.Button", "ctk.CTkButton")
    entry = ("ttk.Entry", "ctk.CTkEntry")
    combo = ("ttk.Combobox", "ctk.CTkCombobox")
    textbox = ("ttk.Textbox", "ctk.CTkTextbox")
    progressbar = ("ttk.Progressbar", "ctk.CTkProgressbar")
    frame = ("ttk.Frame", "ctk.CTkFrame")
    option_menu = ("ttk.OptionMenu", "ctk.CTkOptionMenu")
    radiobutton = ("ttk.Radiobutton", "ctk.CTkRadioButton")
    segemented_button = ("ttk.SegmentedButton", "ctk.CTkSegmentedButton")
    checkbox = ("ttk.CheckBox", "ctk.CTkCheckBox")
    input_dialog = ("ttk.InputDialog", "ctk.CTkInputDialog")
    slider = ("ttk.Slider", "ctk.CTkSlider")
    switch = ("ttk.Switch", "ctk.CTkSwitch")
    image = ("ttk.Image", "ctk.CTkImage")
    toplevel = ("ttk.Toplevel", "ctk.CTkTopLevel")
    regex_config = (".config", ".configure")
    background_color_fix_1 = (", background_color=", "bg_color=")
    foreground_color_fix_1 = (", foreground_color=", "fg_color=")
    background_color_fix_2 = (", background_color = ", "bg_color = ")
    foreground_color_fix_2 = (", foreground_color = ", "fg_color = ")
    all = [import_statement, ttk, ttk2, label, button, entry, combo, textbox, progressbar, frame, option_menu, radiobutton, switch, image, slider, regex_config, background_color_fix_1, background_color_fix_2, foreground_color_fix_1, foreground_color_fix_2]
    tks = [x[0] for x in all]
    ctks = [x[1] for x in all]


@dataclasses.dataclass(slots=True)
class MiscellaneousRegex:
    """ misc regex strings that i have came across
    """
    background_color_1 = re.compile(r'\bbackground_color=')
    background_color_2 = re.compile(r'\bbackground_color =')
    foreground_color_1 = re.compile(r'\bforeground_color=\b')
    foreground_color_2 = re.compile(r'\bforeground_color =\b') 


@dataclasses.dataclass(slots=True)
class MiscellaneousFixes:
    """Misc fixes"""
    background_color_1 = ("background_color=", "bg_color=")
    background_color_2 = ("background_color = ", "bg_color = ")
    foreground_color_1 = ("foreground_color=", "fg_color=")
    foreground_color_2 = ("foreground_color = ", "fg_color = ")


def file_to_lines(tk_file_path: str) -> list[str]:
    """Read a file and return a list of lines with no newline characters

    Args:
        tk_file_path (str): the path to the file to read

    Returns:
        list[str]: a list of lines with no newline characters
    """
    try:
        with open(tk_file_path, 'r') as tk_file:
            lines = [x.strip("\n") for x in tk_file.readlines()]
    except FileNotFoundError:
        return "File not found"
    return lines

def determine_file_structure(lines: list[str]) -> str:
    """Determine the file structure of a list of lines

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        str: one of four possible file structures: Class Based, Void Main, Function Based, or Unknown
    """
    if determine_if_class_based(lines) == True:
        return "Class Based"
    elif determine_if_void_main(lines) == True:
        return "Void Main"
    elif determine_if_function_based(lines) == True:
        return "Function Based"
    else:
        return "Unknown Structure"

def determine_if_class_based(lines: list[str]) -> bool:
    """Determine if a list of lines is a class based file

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        bool: True if the list of lines is a class based file, else False
    """ 
    for line in lines:
        if str(line).startswith("class "):
            if str(line).endswith("Tk):"):
                return True
        if str(line).startswith("\tself.root = tk.Tk()"):
            return True
        if str(line).startswith("\tself.root = Tk()"):
            return True
        if str(line).startswith("\tself.window = Tk()"):
            return True
        if str(line).startswith("\tself.window = tk.Tk()"):
            return True
        if str(line).startswith("\tself.master = Tk()"):
            return True
        if str(line).startswith("\tself.master = tk.Tk()"):
            return True
    return False

def determine_if_void_main(lines: list[str]) -> bool:
    """Determine if a list of lines is a tkinter file in which widgets are defined at the root level.

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        bool: true if the list of lines is a tkinter file in which widgets are defined at the root level, else false
    """
    for line in lines:
        if str(line).startswith("root = Tk()"):
            return True
        if str(line).startswith("root = tk.Tk()"):
            return True
        if str(line).startswith("window = Tk()"):
            return True
        if str(line).startswith("window = tk.Tk()"):
            return True
        if str(line).startswith("master = Tk()"):
            return True
        if str(line).startswith("master = tk.Tk()"):
            return True
    return False

def determine_if_function_based(lines: list[str]) -> bool:
    """Determine if a list of lines is a function based file

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        bool: True if the list of lines is a function based file, else False
    """
    for line in lines:
        if str(line).startswith("\troot = Tk()"):
            return True
        if str(line).startswith("\troot = tk.Tk()"):
            return True
        if str(line).startswith("\twindow = Tk()"):
            return True
        if str(line).startswith("\twindow = tk.Tk()"):
            return True
        if str(line).startswith("\tmaster = Tk()"):
            return True
        if str(line).startswith("\tmaster = tk.Tk()"):
            return True
    return False

def determine_import_type(lines: list[str]) -> str:
    """Determine the import type of a list of lines
        this is dependent on two lines in the file:
            "from tkinter import *"
                    &
            "import tkinter as tk"

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        str: one of four possible import types: 'Type 1', 'Type 2', 'Multiple Types', or 'Unknown'
    """ 
    # declare variables
    type1 = "import tkinter as tk"
    type2 = "from tkinter import *"
    lines_length = len(lines)
    types = [] 
    # shorten lines for processing if necessary
    if lines_length > 10:
        search = lines[:11]
    else:
        search = lines 
    # iterate through lines looking for import statements
    for line in search:
        if str(line).startswith(type1):
            types.append("Type 1")
        if str(line).startswith(type2):
            types.append("Type 2") 
    # determine if there are multiple types
    types = list(set(types))
    types_length = len(types) 
    # return if there are multiple types, or just one type
    if types_length > 1:
        return "Multiple Types"
    elif types_length == 1:
        return types[0] 
    # Panic
    return "Unknown"

def determine_if_program_uses_ttk(lines: list[str]) -> bool:
    """Determine if the given lines contain from tkinter import ttk

    Args:
        lines (list[str]): program lines

    Returns:
        bool: True if the given lines contain from tkinter import ttk
    """
    for line in lines:
        match = re.search(pattern=TtkRegex.import_statement_1, string=line)
        if match:
            return True
    return False

def function_based_ttk(lines: list[str]) -> list[str]:
    """ function based paradigm detected and ttk

    Args:
        lines (list[str]): list of strings from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = TtkRegex
    changer = Change2
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = []
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index+1:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    return converted_lines

def class_based_ttk(lines: list[str]) -> list[str]:
    """ class based paradigm detected type 1

    Args:
        lines (list[str]): list of strings from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = TtkRegex
    changer = TtkChanger
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = []
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index+1:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    return converted_lines

def class_based_2(lines: list[str]) -> list[str]:
    """ class based paradigm detected type 2

    Args:
        lines (list[str]): list of strings from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = Type2Regex
    changer = Change2
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = []
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index+1:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "from customtkinter import *")
    return converted_lines

def class_based_1(lines: list[str]) -> list[str]:
    """ class based paradigm detected type 1

    Args:
        lines (list[str]): list of strings from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = Type1Regex
    changer = Change
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = [] 
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index+1:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "import customtkinter as ctk")
    return converted_lines


def class_based_multiple(lines: list[str]):
    """ classed based and multi-paradigm detected

    Args:
        lines (list[str]): list of lines from the py file

    Returns:
        list[str]: list of lines from the py file
    """
    first_iteration = class_based_1(lines)
    second_iteration = class_based_2(first_iteration)
    return second_iteration

def function_based_2(lines) -> list[str]:
    """ function based paradigm, type 2

    Args:
        lines (list[str]): lines from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = Type2Regex
    changer = Change2
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = [] 
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "from customtkinter import *")
    return converted_lines

def function_based_1(lines: list[str]) -> list[str]:
    """ function based python file is detected

    Args:
        lines (list[str]): lines from the python file

    Returns:
        list[str]: fixed lines from the python file
    """
    regex = Type1Regex
    changer = Change
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = [] 
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index:]
                converted_lines.append(new_line)
                break
            if match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "import customtkinter as ctk")
    return converted_lines

def function_based_multiple(lines):
    """ the file is function based and has multi paradigms

    Args:
        lines (list[str]): lines from the py file

    Returns:
        list[str]: fixed lines from the py file
    """
    first_iteration = function_based_1(lines)
    second_iteration = function_based_2(first_iteration)
    return second_iteration

def void_main_2(lines: list[str]) -> list[str]:
    """ void main type 2 detected

    Args:
        lines (list[str]): list of lines from the file

    Returns:
        list[str]: fixed lines from the file
    """
    regex = Type2Regex
    changer = Change2
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = [] 
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "from customtkinter import *")
    return converted_lines

def void_main_1(lines: list[str]) -> list[str]:
    """ if filetype is void main style

    Args:
        lines (list[str]): lines from the file

    Returns:
        list[str]: fixed lines
    """
    regex = Type1Regex
    changer = Change
    patterns = [
        regex.button, regex.label, regex.frame,
        regex.entry, regex.radiobutton, regex.checkbutton,
        regex.optionmenu, regex.combo, regex.toplevel,
        regex.image
    ]
    changes = [
        changer.button[1], changer.label[1], changer.frame[1],
        changer.entry[1], changer.radiobutton[1], changer.checkbox[1],
        changer.option_menu[1], changer.combo[1], changer.toplevel[1],
        changer.image[1]
    ]
    converted_lines = [] 
    for line in lines:
        my_line = line
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, my_line)
            if match:
                start_index = match.start()
                end_index = match.end()
                new_line = my_line[:start_index] + changes[index] + my_line[end_index:]
                converted_lines.append(new_line)
                break
            elif match is None:
                new_line = my_line
        converted_lines.append(new_line)
    converted_lines.insert(0, "import customtkinter as ctk")
    return converted_lines

def void_main_multiple(lines: list[str]) -> list[str]:
    """ multi-paradigm but void main is present

    Args:
        lines (list[str]): list of lines from the python file

    Returns:
        list[str]: fixed lines from the py file
    """
    first_iteration = void_main_1(lines)
    second_iteration = void_main_2(first_iteration)
    return second_iteration


def determine_mode_of_operation(lines: list[str]) -> tuple[str, str]:
    """Determine the mode of operation of a list of lines by finding the import type and programming paradigm used

    Args:
        lines (list[str]): list of lines from a file

    Returns:
        tuple[str, str]: (<programming paradigm>, <import type>)
    """
    structure = determine_file_structure(lines)
    import_structure = determine_import_type(lines)
    tag = (structure, import_structure)
    return tag

def match_tag(tag: tuple[str, str]) -> any:
    """Match the tuple of string structure and import type to a function

    Args:
        tag (tuple[str, str]): (<script structure>, <import type>)

    Returns:
        any: function to call
    """
    if tag[0] == "Unknown":
         return exit
    if tag[1] == "Unknown":
         return exit
    match tag:
        case ("Class Based", "Type 2"):
            file = class_based_2
        case ("Class Based", "Type 1"):
            file = class_based_1
        case ("Function Based", "Type 2"):
            file = function_based_2
        case ("Function Based", "Type 1"):
            file = function_based_1
        case ("Void Main", "Type 2"):
            file = void_main_2
        case ("Void Main", "Type 1"):
            file = void_main_1
        case ("Class Based", "Multiple Types"):
            file = class_based_multiple
        case ("Function Based", "Multiple Types"):
            file = function_based_multiple
        case ("Void Main", "Multiple Types"):
            file = void_main_multiple
        case other:
            print("Unknown Structures")
            return sys.exit
    return file

def write_new_file(lines: list[str], file_name: str) -> str:
    """Writes a new custom tkinter file with the given lines

    Args:
        lines (list[str]): the newly created customtkinter lines
        file_name (str): the name of the new file

    Returns:
        str: file name
    """
    if not file_name.endswith(".py"):
        file_name = file_name + ".py"
    with open(file_name, "w", encoding='utf-8') as f:
        for line in lines:
            f.write(f"{line}\n")
    return file_name


def ttk_prescan(lines: list[str], tag: tuple[str: str]) -> list[str]:
    """ scan the program lines for ttk evidence, if present, use the tag
    to identify the paradigm and then repair the program lines, return the
    new lines.

    Args:
        lines (list[str]): tkinter program lines
        tag (tuple[str, str]): paradigm and type tuple tags

    Returns:
        list[str]: new repaired list of python program lines
    """
    check_for_ttk = determine_if_program_uses_ttk(lines)
    if check_for_ttk is True:
        if tag[0] == "Class Based":
            return class_based_ttk(lines)
        else:
            return function_based_ttk(lines)
    elif check_for_ttk is False:
        return lines

def convert_tk_to_ctk(tk_file_path: str, ctk_file_path: str) -> str:
    """Converts a tkinter file to a ctk file if possible

    Args:
        tk_file_path (str): path to the tkinter file
        ctk_file_path (str): output path to the ctk file

    Returns:
        str: ctk file path
    """ 
    # get program lines
    lines    = file_to_lines(tk_file_path=tk_file_path)
    # determine paradigm and structure
    tag      = determine_mode_of_operation(lines=lines)
    function = match_tag(tag=tag)
    # exit if panic on paradigm or structure
    if function == exit:
        function()
    # take care of ttk first to prevent tk scans from failing
    post_scan_lines = ttk_prescan(lines, tag)
    # apply the paradigm and structure fixes
    new_lines = function(post_scan_lines)
    write_new_file(lines=new_lines, file_name=ctk_file_path)
    print("New CTK file created ", ctk_file_path)


class TkinterGUI:
    """ Gui class
    """
    def __init__(self):
        """ Initialize the gui
        """
        self.root = tk.Tk()
        self.root.title("tkinter to customtkinter converter")

        # create widgets
        self.file_path_entry = tk.Entry(self.root, width=50)
        self.file_path_entry.grid(row=0, column=0, padx=5, pady=5)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)

        self.output_label = tk.Label(self.root, text="Output file:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5)

        self.output_file_entry = tk.Entry(self.root, width=50)
        self.output_file_entry.grid(row=2, column=0, padx=5, pady=5)
        self.output_file_entry.insert(0, "custom_tkinter_output.py")

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(row=3, column=0, padx=5, pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=3, column=1, padx=5, pady=5)

    def browse_file(self) -> None:
        """ Browse event
        """
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def submit(self) -> None:
        """ submit event
        """
        file_path = self.file_path_entry.get()
        output_file_path = self.output_file_entry.get()
        convert_tk_to_ctk(file_path, output_file_path)
        sys.exit(0)

def gui():
    """ Gui entry point
    """
    gui_version = TkinterGUI()
    gui_version.root.mainloop()

def main():
    """ Application entry point
    """
    filename = __file__.rsplit(os.sep, maxsplit=1)[-1]
    if "-g" in sys.argv:
        gui()
        sys.exit(0) 
    if "-h" in sys.argv:
        print("Tkinter to customtkinter converter\n")
        print(f"Usage: python {filename} <path/to/tkfile> <ctkfile_output_filename>")
        print("options:\n\t -g use the graphical interface\n\t -h help")
        sys.exit(0)
    try:
        args = sys.argv[1:]
    except IndexError:
        print(f"Usage: python {filename} <tkfile> <ctkfile_output_filename>")
        print("please specify the file to convert")
        sys.exit()
    try:
        target = args[0]
    except IndexError:
        print(f"Usage: python {filename} <tkfile> <ctkfile_output_filename>")
        print("please specify the file to convert")
        sys.exit(0)

    path_parts = target.split(os.sep)
    path = str(os.sep).join(path_parts[:-1])

    try:
        output_file = args[1]
        output_path = os.path.join(path, output_file)
    except IndexError:
        output_file = "custom_" + path_parts[-1]
        output_path = os.path.join(path, output_file)
    convert_tk_to_ctk(target, output_path)


if __name__ == "__main__":
    main()

