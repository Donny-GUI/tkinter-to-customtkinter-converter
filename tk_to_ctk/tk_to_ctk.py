import re
import os
import subprocess
import ast

from .util import (
    pip_str,
    get_listbox_source,
    has_listbox,
    classes_begin_index,
    print_warning,
    print_update,
)
from .lists import tkinter_widgets, ctk_widgets
from .templates import print_examples, print_help_screen

# Ensure rich is installed here
try:
    from rich.status import Status
except:
    print(f"rich is not installed. Installing...")
    subprocess.run([pip_str, "install", "rich"], check=True)
    print(f"rich has been installed.")
from rich.status import Status
from rich.console import Console

from .widget_replacer import WidgetReplacer
from .tree import change_orient_to_orientation, change_textvariable_to_variable
from .app_parser import get_parser
from .util import parsetree
from .call import CallArgumentNameChanger, CallArgumentRemover


# Universal Keyword Translations from tkinter to customtkinter
universal_kw_translation = {
    "fg": "fg_color",
    "orient": "orientation",
    "foreground": "fg_color",
    "background": "bg_color",
    "bg": "bg_color",
    "borderwidth": "border_width",
    "text_variable": "textvariable",
    "from": "from_",
    "labelanchor": "label_anchor"
}
# Keywords that are not translated at all from tkinter to customtkinter
not_translated_kws = [
    "selectmode", "blockcursor", "format", "sliderlength", "proxyrelief", "showhandle", "activestyle", "fg", "listvariable", "startline", "class", 
    "show", "labelwidget", "direction", "root", "sliderrelief", "activebackground", "setgrid", "vcmd", "screenName", "endline", "tabs", "spacing3", 
    "className", "default", "selectimage", "phase", "troughcolor", "bigincrement", "label", "tickinterval", "displaycolumns", "useTk", "readonlybackground", 
    "buttonuprelief", "tearoffcommand", "overrelief", "insertunfocussed", "postcommand", "sashcursor", "cnf", "jump", "wraplength", "tabstyle", "sync", 
    "container", "undo", "onvalue", "sashpad", "buttoncursor", "validatecommand", "columns", "maxundo", "opaqueresize", "colormap", "foreground", 
    "disabledforeground", "buttonbackground", "proxyborderwidth", "sashwidth", "padding", "repeatdelay", "baseName", "digits", "activeborderwidth", 
    "activerelief", "offrelief", "validate", "menu", "tristatevalue", "increment", "showvalue", "proxybackground", "justify", "spacing2", "sashrelief", 
    "bitmap", "autoseparators", "style", "invcmd", "maximum", "type", "length", "screen", "resolution", "handlesize", "inactiveselectbackground", "aspect", 
    "buttondownrelief", "disabledbackground", "exportselection", "invalidcommand", "handlepad", "tristateimage", "labelanchor", "spacing1", "visual", 
    "indicatoron", "selectcolor", "exists", "tearoff", "elementborderwidth", "use", "activeforeground", "repeatinterval"
]
# List of widgets available in customtkinter 
ctk_widget_names = [
    "CTk",
    "CTkInputDialog",
    "CTkToplevel",
    "CTkButton",
    "CTkCheckBox",
    "CTkComboBox",
    "CTkEntry",
    "CTkFrame",
    "CTkLabel",
    "CTkOptionMenu",
    "CTkProgressBar",
    "CTkRadioButton",
    "CTkScrollableFrame",
    "CTkScrollbar",
    "CTkSegmentedButton",
    "CTkSlider",
    "CTkSwitch",
    "CTkTabview",
    "CTkFrames",
    "CTkTextbox",
]
# list of widgets available in customtkinter when using different import styles
ctk_qualified_widget_names = ["ctk." + x for x in ctk_widget_names]



tk_widget_arguments = {
    "tk.Tk":            ["screenName", "baseName", "className", "useTk", "sync", "use"],
    "ttk.Button":        ["command", "default", "takefocus", "text", "textvariable", "underline", 
                        "width", "image", "compound", "padding", "state", "cursor", "style", "class"],
    "ttk.Checkbox":      ["variable", "onvalue", "offvalue", "command", "takefocus", "text", "textvariable", 
                        "underline", "width", "image", "compound", "padding", "state", "cursor", "style", "class" ],
    "ttk.Combobox":      ["height", "postcommand", "values", "exportselection", "font", "invalidcommand", "justify", 
                        "show", "state", "textvariable", "validate", "validatecommand", "width", "xscrollcommand", 
                        "foreground", "background", "takefocus", "cursor", "style", "class"],
    "ttk.Entry":         ["exportselection", "font", "invalidcommand", "justify", "show", "state", "textvariable", 
                        "validate", "validatecommand", "width", "xscrollcommand", "foreground", "background", 
                        "takefocus", "cursor", "style"],
    "ttk.Label":         ["background", "bg", "fg", "foreground", "font", "borderwidth", "relief", "anchor", "justify", 
                        "wraplength", "takefocus", "text", "textvariable", "underline", "width", "image", "compound", 
                        "padding", "state", "cursor", "style"],
    "ttk.LabeledScale": ["borderwidth", "padding", "relief", "width", "height", "takefocus", "cursor", "style"],
    "ttk.Labelframe":   ["labelanchor", "text", "underline", "labelwidget", "borderwidth", "padding", "relief", 
                         "width", "height", "takefocus", "cursor", "style"],
    "ttk.Menubutton":   ["menu", "direction", "takefocus", "text", "textvariable", "underline", "width", 
                        "image", "compound", "padding", "state", "cursor", "style"],
    "ttk.Notebook":     ["height", "padding", "takefocus", "cursor", "style"],
    "ttk.Panedwindow":  ["orient", "width", "height", "takefocus", "cursor", "style"],
    "ttk.Progressbar":  ["orient", "length", "mode", "maximum", "value", "variable", "phase", "takefocus", "cursor", "style"],
    "ttk.Radiobutton":  ["variable", "value", "command", "takefocus", "text", "textvariable", "underline", 
                        "width", "image", "compound", "padding", "state", "cursor", "style"],
    "ttk.Scale":        ["orient", "length", "from", "to", "variable", "command", "takefocus", "cursor", "style"],
    "ttk.Scrollbar":    ["command", "orient", "takefocus", "cursor", "style"],
    "ttk.Separator":    ["orient", "takefocus", "cursor", "style"],
    "ttk.Spinbox":      ["values", "from", "to", "increment", "format", "command", "wrap", "exportselection", "font", 
                        "invalidcommand", "justify", "show", "state", "textvariable", "validate", "validatecommand", 
                        "width", "xscrollcommand", "foreground", "background", "takefocus", "cursor", "style"],
    "ttk.Treeview":     ["columns", "displaycolumns", "show", "selectmode", "height", "padding", "xscrollcommand", 
                        "yscrollcommand", "takefocus", "cursor", "style"],
    
    "tk.Canvas":        ["background", "bd", "bg", "borderwidth", "closeenough", "confine", "cursor", "height", 
                        "highlightbackground", "highlightcolor", "highlightthickness", "insertbackground", "insertborderwidth", 
                        "insertofftime", "insertontime", "insertwidth", "offset", "relief", "scrollregion", "selectbackground", 
                        "selectborderwidth", "selectforeground", "state", "takefocus", "width", "xscrollcommand", "xscrollincrement", 
                        "yscrollcommand", "yscrollincrement"],
    "tk.Listbox":       ["activestyle", "background", "bd", "bg", "borderwidth", "cursor", "disabledforeground", 
                        "exportselection", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", 
                        "highlightthickness", "justify", "relief", "selectbackground", "selectborderwidth", "selectforeground", 
                        "selectmode", "setgrid", "state", "takefocus", "width", "xscrollcommand", "yscrollcommand", "listvariable"],
    "tk.Menu":          ["activebackground", "activeborderwidth", "activeforeground", "background", "bd", "bg", "borderwidth", 
                        "cursor", "disabledforeground", "fg", "font", "foreground", "postcommand", "relief", "selectcolor", 
                        "takefocus", "tearoff", "tearoffcommand", "title", "type"],
    "tk.Text":          ["autoseparators", "background", "bd", "bg", "blockcursor", "borderwidth", "cursor", "endline", 
                        "exportselection", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", 
                        "highlightthickness", "inactiveselectbackground", "insertbackground", "insertborderwidth", "insertofftime", 
                        "insertontime", "insertunfocussed", "insertwidth", "maxundo", "padx", "pady", "relief", "selectbackground", 
                        "selectborderwidth", "selectforeground", "setgrid", "spacing1", "spacing2", "spacing3", "startline", "state", 
                        "tabs", "tabstyle", "takefocus", "undo", "width", "wrap", "xscrollcommand", "yscrollcommand"],
    "tk.Toplevel":      ["bd", "borderwidth", "class", "menu", "relief", "screen", "use", "background", "bg", "colormap", 
                        "container", "cursor", "height", "highlightbackground", "highlightcolor", "highlightthickness", 
                        "padx", "pady", "takefocus", "visual", "width"],
    "tk.Button":        ["activebackground", "activeforeground", "anchor", "background", "bd", "bg", "bitmap", "borderwidth", 
                         "command", "compound", "cursor", "default", "disabledforeground", "fg", "font", "foreground", "height", 
                         "highlightbackground", "highlightcolor", "highlightthickness", "image", "justify", "overrelief", "padx", 
                         "pady", "relief", "repeatdelay", "repeatinterval", "state", "takefocus", "text", "textvariable", "underline", 
                         "width", "wraplength"],
    "tk.Checkbutton":   ["activebackground", "activeforeground", "anchor", "background", "bd", "bg", "bitmap", "borderwidth", "command", "compound", "cursor", "disabledforeground", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", "highlightthickness", "image", "indicatoron", "justify", "offrelief", "offvalue", "onvalue", "overrelief", "padx", "pady", "relief", "selectcolor", "selectimage", "state", "takefocus", "text", "textvariable", "tristateimage", "tristatevalue", "underline", "variable", "width", "wraplength"],
    "tk.Entry":         ["background", "bd", "bg", "borderwidth", "cursor", "disabledbackground", "disabledforeground", "exportselection", "fg", "font", "foreground", "highlightbackground", "highlightcolor", "highlightthickness", "insertbackground", "insertborderwidth", "insertofftime", "insertontime", "insertwidth", "invalidcommand", "invcmd", "justify", "readonlybackground", "relief", "selectbackground", "selectborderwidth", "selectforeground", "show", "state", "takefocus", "textvariable", "validate", "validatecommand", "vcmd", "width", "xscrollcommand"],
    "tk.Frame":         ["bd", "borderwidth", "class", "relief", "background", "bg", "colormap", "container", "cursor", "height", "highlightbackground", "highlightcolor", "highlightthickness", "padx", "pady", "takefocus", "visual", "width"],
    "tk.Label":         ["activebackground", "activeforeground", "anchor", "background", "bd", "bg", "bitmap", "borderwidth", "compound", "cursor", "disabledforeground", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", "highlightthickness", "image", "justify", "padx", "pady", "relief", "state", "takefocus", "text", "textvariable", "underline", "width", "wraplength"],
    "tk.Labelframe":    ["bd", "borderwidth", "class", "fg", "font", "foreground", "labelanchor", "labelwidget", "relief", "text", "background", "bg", "colormap", "container", "cursor", "height", "highlightbackground", "highlightcolor", "highlightthickness", "padx", "pady", "takefocus", "visual", "width"],
    "tk.Menubutton":    ["activebackground", "activeforeground", "anchor", "background", "bd", "bg", "bitmap", "borderwidth", "cursor", "direction", "disabledforeground", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", "highlightthickness", "image", "indicatoron", "justify", "menu", "padx", "pady", "relief", "compound", "state", "takefocus", "text", "textvariable", "underline", "width", "wraplength"],
    "tk.Message":       ["anchor", "aspect", "background", "bd", "bg", "borderwidth", "cursor", "fg", "font", "foreground", "highlightbackground", "highlightcolor", "highlightthickness", "justify", "padx", "pady", "relief", "takefocus", "text", "textvariable", "width"],
    "tk.OptionMenu":    ["master", "variable", "value", "*", "**"],
    "tk.PanedWindow":   ["background", "bd", "bg", "borderwidth", "cursor", "handlepad", "handlesize", "height", "opaqueresize", "orient", "proxybackground", "proxyborderwidth", "proxyrelief", "relief", "sashcursor", "sashpad", "sashrelief", "sashwidth", "showhandle", "width"],
    "tk.Radiobutton":   ["activebackground", "activeforeground", "anchor", "background", "bd", "bg", "bitmap", "borderwidth", "command", "compound", "cursor", "disabledforeground", "fg", "font", "foreground", "height", "highlightbackground", "highlightcolor", "highlightthickness", "image", "indicatoron", "justify", "offrelief", "overrelief", "padx", "pady", "relief", "selectcolor", "selectimage", "state", "takefocus", "text", "textvariable", "tristateimage", "tristatevalue", "underline", "value", "variable", "width", "wraplength"],
    "tk.Scale":         ["activebackground", "background", "bigincrement", "bd", "bg", "borderwidth", "command", "cursor", "digits", "fg", "font", "foreground", "from", "highlightbackground", "highlightcolor", "highlightthickness", "label", "length", "orient", "relief", "repeatdelay", "repeatinterval", "resolution", "showvalue", "sliderlength", "sliderrelief", "state", "takefocus", "tickinterval", "to", "troughcolor", "variable", "width", ],
    "tk.Scrollbar":     ["activebackground", "activerelief", "background", "bd", "bg", "borderwidth", "command", "cursor", "elementborderwidth", "highlightbackground", "highlightcolor", "highlightthickness", "jump", "orient", "relief", "repeatdelay", "repeatinterval", "takefocus", "troughcolor", "width"],
    "tk.Spinbox":       ["activebackground", "background", "bd", "bg", "borderwidth", "buttonbackground", "buttoncursor", "buttondownrelief", "buttonuprelief", "command", "cursor", "disabledbackground", "disabledforeground", "exportselection", "fg", "font", "foreground", "format", "from", "highlightbackground", "highlightcolor", "highlightthickness", "increment", "insertbackground", "insertborderwidth", "insertofftime", "insertontime", "insertwidth", "invalidcommand", "invcmd", "justify", "relief", "readonlybackground", "repeatdelay", "repeatinterval", "selectbackground", "selectborderwidth", "selectforeground", "state", "takefocus", "textvariable", "to", "validate", "validatecommand", "values", "vcmd", "width", "wrap", "xscrollcommand"],
    "tk.Variable":      ["master", "value", "name"],
    "tk.BoolenVar":     ["master", "value", "name"],
    "tk.DoubleVar":     ["master", "value", "name"],
    "tk.IntVar":        ["master", "value", "name"],
    "tk.StringVar":     ["master", "value", "name"],
    "tk.BitmapImage":   ["name", "cnf", "master", "**"],
    "tk.PhotoImage":    ["name", "cnf", "master", "**"],
    "tk.filedialog.Directory": ["master", "**"],
    "tk.filedialog.Open": ["master", "**"],
    "tk.filedialog.SaveAs": ["master", "**"],
    "tk.colorchooser.Chooser": ["master", "**"],
    "ttk.Style":        ["master"],
    "ttk.Font":         ["root", "font", "name", "exists", "**"],
}
ctk_widget_arguments = {
    "ctk.CTkButton":                ["master", "width", "height", "corner_radius", "border_width", "border_spacing", "fg_color", "hover_color", "border_color", "text_color", "text_color_disabled", "text", "font", "textvariable", "image", "state", "hover", "command", "compound", "anchor"],
    "ctk.CTk":                      ["fg_color"],
    "ctk.CTkInputDialog":           ["title", "text", "fg_color", "button_hover_color", "button_text_color", "entry_fg_color", "entry_border_color", "entry_text_color" ],
    "ctk.CTkToplevel":              ["fg_color"],
    "ctk.CTkCheckBox":              ["master", "width", "height", "checkbox_width", "corner_radius", "border_width", "fg_color", "border_color", "text_color", "text", "textvariable", "font", "hover", "state", "variable", "offvalue" ],
    "ctk.CTkComboBox":              ["master", "width", "height", "corner_radius", "border_width", "fg_color", "border_color", "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color", "text_color", "font", "dropdown_font", "values", "hover", "state", "variable" ],
    "ctk.CTkEntry":                 ["master", "textvariable", "width", "height", "corner_radius", "fg_color", "text_color", "placeholder_text_color", "placeholder_text", "font", "state" ],
    "ctk.CTkFrame":                 ["master", "width", "height", "border_width", "fg_color", "border_color" ],
    "ctk.CTkLabel":                 ["master", "textvariable", "text", "width", "height", "corner_radius", "fg_color", "text_color", "font", "anchor", "compound", "padx", "pady" ],
    "ctk.CTkOptionMenu":            ["master", "width", "height", "corner_radius", "fg_color", "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color", "text_color", "font", "dropdown_font", "hover", "state", "variable", "values", "dynamic_resizing", "anchor" ],
    "ctk.CTkProgressBar":           ["master", "width", "height", "border_width", "corner_radius", "fg_color", "border_color", "progress_color", "mode", "determinate_speed" ],
    "ctk.CTkRadioButton":           ["master", "width", "height", "radiobutton_width", "radiobutton_height", "corner_radius", "border_width_unchecked", "border_width_checked", "fg_color", "border_color", "text_color", "text", "textvariable", "font", "hover", "state", "variable", "value" ],
    "ctk.CTkScrollableFrame":       ["master", "width", "height", "corner_radius", "border_width", "fg_color", "border_color", "scrollbar_fg_color", "scrollbar_button_color", "scrollbar_button_hover_color", "label_fg_color", "label_text_color", "label_text", "label_font", "label_anchor" ],
    "ctk.CTkScrollbar":             ["master", "width", "height", "corner_radius", "border_spacing", "fg_color", "button_color", "button_hover_color", "minimum_pixel_length", "hover" ],
    "ctk.CTkSegmentedButton":       ["master", "width", "height", "corner_radius", "border_width", "fg_color", "selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color", "text_color", "font", "values", "variable", "state", "dynamic_resizing" ],
    "ctk.CTkSlider":                ["master", "variable", "width", "height", "border_width", "from_", "to", "fg_color", "progress_color", "border_color", "button_color", "button_hover_color", "state", "hover" ],
    "ctk.CTkSwitch":                ["master", "width", "height", "switch_width", "switch_height", "corner_radius", "border_width", "fg_color", "border_color", "progress_color", "button_color", "button_hover_color", "text_color", "text", "textvariable", "font", "variable", "offvalue", "statemaster", "width", "height", "switch_width", "switch_height", "corner_radius", "border_width", "fg_color", "border_color", "progress_color", "button_color", "button_hover_color", "text_color", "text", "textvariable", "font", "variable", "offvalue", "state" ],
    "ctk.CTkTabview":               ["master", "width", "height", "corner_radius", "border_width", "fg_color", "border_color", "segmented_button_fg_color", "segmented_button_selected_hover_color", "segmented_button_unselected_color", "text_color", "anchor", "state" ],
    "ctk.CTkTextbox":               ["master", "width", "height", "corner_radius", "border_width", "border_spacing", "fg_color", "border_color", "text_color", "scrollbar_button_color", "scrollbar_button_hover_color", "font", "state", "wrap" ],
    "ctk.CTkFont":                  ["family", "size", "weight", "slant", "underline", "overstrike"],
    "ctk.CTkImage":                 ["light_image", "dark_image", "size"],
    "ctk.CTkCanvas":                ["background", "bd", "bg", "borderwidth", "closeenough", "confine", "cursor", "height",  "highlightbackground", "highlightcolor", "highlightthickness", "insertbackground", "insertborderwidth",  "insertofftime", "insertontime", "insertwidth", "offset", "relief", "scrollregion", "selectbackground",  "selectborderwidth", "selectforeground", "state", "takefocus", "width", "xscrollcommand", "xscrollincrement",  "yscrollcommand", "yscrollincrement"],
    "ctk.Variable":                 ["master", "value", "name"],
    "ctk.BoolenVar":                ["master", "value", "name"],
    "ctk.DoubleVar":                ["master", "value", "name"],
    "ctk.IntVar":                   ["master", "value", "name"],
    "ctk.StringVar":                ["master", "value", "name"],
    "ctk.filedialog.Directory":     ["master", "**"],
    "ctk.filedialog.Open":          ["master", "**"],
    "ctk.filedialog.SaveAs":        ["master", "**"],
    "ctk.colorchooser.Chooser":     ["master", "**"],
    "ctk.CTkVariable":              ["master", "value", "name"],
    "ctk.CTkVariable":                 ["master", "value", "name"],
    "ctk.CTkBoolenVar":                ["master", "value", "name"],
    "ctk.CTkDoubleVar":                ["master", "value", "name"],
    "ctk.CTkIntVar":                   ["master", "value", "name"],
    "ctk.CTkStringVar":                ["master", "value", "name"],
    "ctk.CTkPhotoImage":               ["master", "light_image", "dark_image", "size"],  
}

ctk_cant_have_these_keywords = {
    'ctk.CTk': ['screenName', 'baseName', 'className', 'useTk', 'sync', 'use'],
    'ctk.CTkButton': ['activebackground',
                   'activeforeground',
                   'bd',
                   'bitmap',
                   'cursor',
                   'default',
                   'disabledforeground',
                   'highlightbackground',
                   'highlightcolor',
                   'highlightthickness',
                   'justify',
                   'overrelief',
                   'padx',
                   'pady',
                   'relief',
                   'repeatdelay',
                   'repeatinterval',
                   'takefocus',
                   'underline',
                   'wraplength'],
    'ctk.CTkCanvas': [],
    'ctk.CTkCheckBox': ['activebackground',
                     'activeforeground',
                     'anchor',
                     'bd',
                     'bitmap',
                     'command',
                     'compound',
                     'cursor',
                     'disabledforeground',
                     'highlightbackground',
                     'highlightcolor',
                     'highlightthickness',
                     'image',
                     'indicatoron',
                     'justify',
                     'offrelief',
                     'onvalue',
                     'overrelief',
                     'padx',
                     'pady',
                     'relief',
                     'selectcolor',
                     'selectimage',
                     'takefocus',
                     'tristateimage',
                     'tristatevalue',
                     'underline',
                     'wraplength'],
    'ctk.CTkComboBox': ['postcommand',
                     'exportselection',
                     'invalidcommand',
                     'justify',
                     'show',
                     'textvariable',
                     'validate',
                     'validatecommand',
                     'xscrollcommand',
                     'takefocus',
                     'cursor',
                     'style',
                     'class'],
    'ctk.CTkDoubleVar': [],
    'ctk.CTkEntry': ['bd',
                  'cursor',
                  'disabledbackground',
                  'disabledforeground',
                  'exportselection',
                  'highlightbackground',
                  'highlightcolor',
                  'highlightthickness',
                  'insertbackground',
                  'insertborderwidth',
                  'insertofftime',
                  'insertontime',
                  'insertwidth',
                  'invalidcommand',
                  'invcmd',
                  'justify',
                  'readonlybackground',
                  'relief',
                  'selectbackground',
                  'selectborderwidth',
                  'selectforeground',
                  'show',
                  'takefocus',
                  'validate',
                  'validatecommand',
                  'vcmd',
                  'xscrollcommand'],
    'ctk.CTkFrame': ['bd',
                  'class',
                  'relief',
                  'colormap',
                  'container',
                  'cursor',
                  'highlightbackground',
                  'highlightcolor',
                  'highlightthickness',
                  'padx',
                  'pady',
                  'takefocus',
                  'visual'],
    'ctk.CTkImage': ['name', 'cnf', 'master', '**'],
    'ctk.CTkIntVar': [],
    'ctk.CTkLabel': ['activebackground',
                  'activeforeground',
                  'bd',
                  'bitmap',
                  'cursor',
                  'disabledforeground',
                  'highlightbackground',
                  'highlightcolor',
                  'highlightthickness',
                  'image',
                  'justify',
                  'relief',
                  'state',
                  'takefocus',
                  'underline',
                  'wraplength'],
    'ctk.CTkOptionMenu': ['value', '*', '**'],
    'ctk.CTkPhotoImage': ['name', 'cnf', '**'],
    'ctk.CTkProgressBar': ['length',
                        'maximum',
                        'value',
                        'variable',
                        'phase',
                        'takefocus',
                        'cursor',
                        'style'],
    'ctk.CTkRadioButton': ['activebackground',
                        'activeforeground',
                        'anchor',
                        'bd',
                        'bitmap',
                        'command',
                        'compound',
                        'cursor',
                        'disabledforeground',
                        'highlightbackground',
                        'highlightcolor',
                        'highlightthickness',
                        'image',
                        'indicatoron',
                        'justify',
                        'offrelief',
                        'overrelief',
                        'padx',
                        'pady',
                        'relief',
                        'selectcolor',
                        'selectimage',
                        'takefocus',
                        'tristateimage',
                        'tristatevalue',
                        'underline',
                        'wraplength'],
    'ctk.CTkScrollableFrame': ['text',
                            'underline',
                            'labelwidget',
                            'padding',
                            'relief',
                            'takefocus',
                            'cursor',
                            'style'],
    'ctk.CTkScrollbar': ['activebackground',
                      'activerelief',
                      'bd',
                      'command',
                      'cursor',
                      'elementborderwidth',
                      'highlightbackground',
                      'highlightcolor',
                      'highlightthickness',
                      'jump',
                      'relief',
                      'repeatdelay',
                      'repeatinterval',
                      'takefocus',
                      'troughcolor'],
    'ctk.CTkSlider': ['activebackground',
                   'bigincrement',
                   'bd',
                   'command',
                   'cursor',
                   'digits',
                   'font',
                   'highlightbackground',
                   'highlightcolor',
                   'highlightthickness',
                   'label',
                   'length',
                   'relief',
                   'repeatdelay',
                   'repeatinterval',
                   'resolution',
                   'showvalue',
                   'sliderlength',
                   'sliderrelief',
                   'takefocus',
                   'tickinterval',
                   'troughcolor'],
    'ctk.CTkStringVar': [],
    'ctk.CTkTabview': ['takefocus', 'cursor', 'style'],
    'ctk.CTkTextbox': ['autoseparators',
                    'bd',
                    'blockcursor',
                    'cursor',
                    'endline',
                    'exportselection',
                    'highlightbackground',
                    'highlightcolor',
                    'highlightthickness',
                    'inactiveselectbackground',
                    'insertbackground',
                    'insertborderwidth',
                    'insertofftime',
                    'insertontime',
                    'insertunfocussed',
                    'insertwidth',
                    'maxundo',
                    'padx',
                    'pady',
                    'relief',
                    'selectbackground',
                    'selectborderwidth',
                    'selectforeground',
                    'setgrid',
                    'spacing1',
                    'spacing2',
                    'spacing3',
                    'startline',
                    'tabs',
                    'tabstyle',
                    'takefocus',
                    'undo',
                    'xscrollcommand',
                    'yscrollcommand'],
    'ctk.CTkToplevel': ['bd',
                     'class',
                     'menu',
                     'relief',
                     'screen',
                     'use',
                     'colormap',
                     'container',
                     'cursor',
                     'height',
                     'highlightbackground',
                     'highlightcolor',
                     'highlightthickness',
                     'padx',
                     'pady',
                     'takefocus',
                     'visual',
                     'width'],
    'ctk.CTkVariable': []
}
all_unused_params = []
[all_unused_params.extend(value) for value in ctk_cant_have_these_keywords.values()]


    

Gverbose = False

##################################################
# FUNCTIONS
##################################################

def verbose_print(string: str) -> None:
    global Gverbose
    if Gverbose:
        print(string)


def fix_orient_and_textvar_calls(file_path: str) -> None:
    """
    Description:
        Takes a file path and replaces all the
        'orient="' -> orientation=" and
        "textvariable" to "variable" parameters
        for compatibility with customtkinter.
    Arguments:
        file_path (str): path to the file
    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    source = change_textvariable_to_variable(content)
    source = change_orient_to_orientation(source)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(source)


def replace_bg_with_bg_color_in_file(file_path: str) -> None:
    """
    Description:
        Takes a file path and replaces all the 'bg="red"' -> bg_color="red"
        parameters for compatibility with customtkinter.
    Arguments:
        file_path (str): path to the file
    Returns:
        None
    """
    global Gverbose

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    cont = content.replace(", bg=", ", bg_color=").replace(", bg =", ", bg_color =")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)


def replace_fg_with_fg_color_in_file(file_path: str) -> None:
    """
    Description:
        Takes a file path and replaces all the 'fg="red"' -> fg_color="red"
        parameters for compatibility with customtkinter.
    Arguments:
        file_path (str): path to the file
    Returns:
        None
    """
    verbose_print(f"Reading {file_path}...")
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    verbose_print("Replacing fg in content...")
    cont = content.replace(", fg=", ", fg_color=").replace(", fg =", ", fg_color =")
    verbose_print(f"Writing content to file : {file_path}...")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)


def replace_meta_in_file(file_path: str) -> None:
    """
    Description:
        Replace all the tk meta class or base classes
        with custom tkinter ones.
    Arguments:
        file_path (str): path to file to be replaced
    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    verbose_print(f"{file_path} read.")
    cont = content.replace(r"(tk.Tk):", r"(ctk.CTk):")
    verbose_print("meta and base tk classes replaced...")
    for index, widget in enumerate(tkinter_widgets):
        verbose_print(f"finding base class widget {widget}...")
        cont = cont.replace(f"(tk.{widget}):", f"(ctk.{ctk_widgets[index]}):")
    cont = cont.replace("(Tk):", "(ctk.CTk):")
    cont = cont.replace("Tk()", "ctk.CTk()")
    verbose_print(f"Writing new content to {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)


def replace_config_with_configure(file_path: str) -> None:
    """
    Description:
        Takes a file path and replaces all the widget.config() -> widget.configure()
        methods for compatibility with customtkinter.
    Arguments:
        file_path (str): path to the file
    Returns:
        None
    """
    verbose_print(f"Reading {file_path}")
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    verbose_print(f"Read {file_path}")
    verbose_print(f"Substituting .config --> .configure")
    modified_content = re.sub(r"\.config\(", ".configure(", content)
    verbose_print(f"Writing {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(modified_content)


def find_errs(file_path: str) -> None:
    """
    Description:
        Find errors in the tk-ctk psuedo code. Takes a python like code and
        ensures that all errors are corrected and converted.
    Arguments:
        file_path (str): path to file to find errors in
    Returns:
        None
    """
    verbose_print(f"Reading lines: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        retv = []

        verbose_print("Substituting by line....")
        for line in lines:
            verbose_print("old line: \n" + line)
            l = re.sub(r"ttk.ctk.", r"ctk.", line)
            l2 = re.sub(r"tk.ctk.", r"ctk.", l)
            l3 = re.sub(r".CTkText", r".CTkTextbox", l2)
            l4 = re.sub(r".CTkRadiobutton", r".CTkRadioButton", l3)
            # CTkCheckButton
            l5 = re.sub(r".CTkCheckbutton", r".CTkCheckBox", l4)
            l6 = re.sub(r".CTkScale", r".CTkSlider", l5)
            l7 = l6
            verbose_print(f"new line: \n" + l7)
            retv.append(l7)

    verbose_print(f" Writing {file_path}")
    with open(file_path, "w", encoding="utf-8") as wfile:
        for l in retv:
            wfile.write(l)


def rewrite_listboxes(filepath: str) -> None:
    """
    Description:
        Add the listbox class for custom tkinter
        and convert all the tk.Listbox -> CTkListbox.
    Arguments:
        filepath (str): path to file to be rewritten
    Returns:
        None
    """
    final_lines = []
    # does the file even have listboxes?
    if has_listbox(filepath) == True:

        # get the source lines to add to for the ListBox class
        listbox_addition = get_listbox_source()
        # read the source lines
        with open(filepath, "r") as r:
            source_lines = r.readlines()
        # determine where the classes should begin
        class_index = classes_begin_index(source_lines)

        # inject the class at the class index
        for index, line in enumerate(source_lines):
            if index == class_index:
                for source_line in listbox_addition:
                    final_lines.append(source_line)
            final_lines.append(line)

        # write the lines out
        with open(filepath, "w") as w:
            w.writelines(final_lines)
        # read the new content from the class injection
        with open(filepath, "r") as r:
            content = r.read()
        # substitute the listboxes for the CTkListbox
        content2 = re.sub(r"tk\.Listbox(?!\()", r" CTkListbox", content)
        content3 = re.sub(
            r"customtkinter\.ThemeManager\.", "ctk.ThemeManager.", content2
        )
        # write the final content
        with open(filepath, "w") as w:
            w.write(content3)

def remove_relief_from_CTkButton(content: str) -> str:
    tree = parsetree(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == "ctk.CTkButton" or string_name == "CTkButton":
                node.keywords = [kw for kw in node.keywords if kw.arg != "relief"]
    return ast.unparse(tree) 

def remove_parameter_from_calls_with_names(node_names:list[str], content: str, parameter: str) -> str:
    tree = parsetree(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            for name in node_names:
                if name in string_name:
                    node.keywords = [kw for kw in node.keywords if kw.arg != parameter]
                    break
            
    return ast.unparse(tree)

def change_parameter_in_calls_with_names(node_names:list[str], content: str, parameter: str, new_parameter: str) -> str:
    tree = parsetree(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            for name in node_names:
                if name in string_name:
                    node.keywords = [kw for kw in node.keywords if kw.arg != parameter]
                    node.keywords.append(ast.keyword(arg=new_parameter, value=node.keywords[0].value))
                    break
            
    return ast.unparse(tree)

def change_call_func_name(func_name:str, new_name:str, content: str) -> str:
    tree = parsetree(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == func_name:
                if isinstance(node.func, ast.Name):
                    node.func.id = new_name
                elif isinstance(node.func, ast.Attribute):
                    attr, value = new_name.split(".", 1)
                    node.func.attr = attr
                    node.func.value.id = value

    return ast.unparse(tree)

def remove_parameter_for_call(parameter:str, call_name:str, content: str) -> str:
    tree = parsetree(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == call_name:
                node.keywords = [kw for kw in node.keywords if kw.arg != parameter]

    return ast.unparse(tree)


def remove_keyword_from_line(line:str, keyword:str) -> str:
    start_kw = line.index(keyword)
    end_kw = start_kw + len(keyword)
    length = len(line) - 1
    c = end_kw
    while c < length:
        
        char = line[c]
        c+=1
        
        if char == ")":
            c+=1
            break

        elif char == ",":
            c+=1
            break

        elif char == "(":
            c+=1
            while char != ")":
                char = line[c]
                c+=1
            
        elif char == "'" or char == '"':
            
            save = char
            c+=1
            while char != save:
                char = line[c]
                c+=1

        elif char == "[":
            
            save = "]"
            c+=1
            while char != save:
                char = line[c]
                c+=1
    
    xline = str(line[:start_kw] + line[c:-1]).strip()
    if xline.endswith(","):
        return xline[:-1] + ")"
    
    if xline.endswith(")"):
        return xline
    else:
        return line[:start_kw] + line[c:-1] + ")"
    
 
    

def make_custom_tkinter(
    input_file: str,
    output_filename: str,
    convert_listboxes: bool = False,
    verbose: str = False,
) -> None:
    """
    Description:
        Create a customtkinter file from a tkinter file
    Arguments:
        input_file (str): the tkinter file to use
        output_filename (str): the desired output file
    Returns:
        None
    """
    con = Console()
    with Status(f"Analyzing {input_file}...") as status:
        verbose_print("Creating instance of WidgetReplacer class...")
        wr = WidgetReplacer(input_file, output_filename)

        verbose_print("iterating through tkinter widgets to add ctk regex patterns...")
        for widget in tkinter_widgets:
            ctk_widget = f"ctk.CTk{widget}"
            verbose_print(widget)
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

        verbose_print("iterating through tkinter widgets to add tk regex patterns...")
        for widg in tkinter_widgets:
            widget = "tk." + widg
            verbose_print(widget)
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
        status.update(" ttk.Widget -> ctk.CTkWidget")

        verbose_print("Iterating through ttk widgets for regex patterns...")
        for widg in tkinter_widgets:
            widget: str = "ttk." + widg
            ctk_widget: str = f"ctk.CTk{widg}"
            verbose_print(widget)
            wr.add_findable("{0}(".format(widget), "{0}(".format(ctk_widget))
            wr.add_findable("{0}, ".format(widget), "")
            wr.add_findable(widget + ",", "{0},".format(ctk_widget))
            wr.add_findable(" = {0}(".format(widget), " = {0}(".format(ctk_widget))
            wr.add_findable("={0}(".format(widget), "={0}(".format(ctk_widget))
            wr.add_findable(": {0} ".format(widget), ": {0} ".format(ctk_widget))
            wr.add_findable(":{0},".format(widget), ":{0},".format(ctk_widget))
            wr.add_findable(":{0}".format(widget), ":{0}".format(ctk_widget))

        verbose_print("Replacing all widgets now...")
        status.update("Replacing all widgets...")
        wr.replace_widgets()

        verbose_print("Double checking widgets now...")
        status.update("Double checking constants...")
        wr.double_check()

        status.update("finding .config/.configure...")
        verbose_print("Finding .config/.configure to replace...")
        replace_config_with_configure(file_path=output_filename)

        status.update("finding bg/bg_color...")
        verbose_print("finding bg parameter to convert to bg_color...")
        replace_bg_with_bg_color_in_file(file_path=output_filename)

        status.update("finding fg/fg_color...")
        verbose_print("finding fg parameter to convert to fg_color")
        replace_fg_with_fg_color_in_file(file_path=output_filename)

        status.update("    finding meta class options...")
        verbose_print("finding meta class tkinter objects...")
        replace_meta_in_file(file_path=output_filename)

        status.update("Checking for errors...")
        verbose_print("checking for errors...")
        find_errs(file_path=output_filename)

        if convert_listboxes:
            status.update(" fixing the listboxes...")
            verbose_print("Converting listboxes as specified by listbox flag...")
            rewrite_listboxes(filepath=output_filename)

        ## have to be try statements because it uses ast.parse and ast.unparse
        #try:
        #    status.update("Fixing textvariable and orient call parameters...")
        #    fix_orient_and_textvar_calls(filepath=output_filename)
        #except:
        #    verbose_print("Could not fix 'textvariable' and 'orient' call parameters")
        #
        #try:
        #    status.update("Fixing resolution parameters for CTkSlider...")
        #    remove_resolution_parameter_for_ctk_slider(filepath=output_filename)
        #except:
        #    verbose_print("Could not remove resolution parameter from CTkSlider")
        
        
        with open(output_filename, "r", errors="ignore") as f:
            source = f.read()

        
        try:
            tree = ast.parse(source)
        except SyntaxError:
            verbose_print("SyntaxError")
            con.print("Cannot Parse file!")
            exit(1)
    
        con.print("Fixing call parameters...")
        call_argument_changer = CallArgumentNameChanger()
        call_argument_remover = CallArgumentRemover()
        status.update("Fixing call parameters...")
        
        # Iterate through all ctk widgets and change their call parameters
        for ctkwidget in ctk_widgets:
            # Add universal keyword translations
            for oldkw, newkw in universal_kw_translation.items():
                call_argument_changer.add_argument_name_change(ctkwidget, oldkw, newkw)
            
            if ctk_cant_have_these_keywords.get(ctkwidget, None):
                # Add specific keyword removals for each widget
                for kw in ctk_cant_have_these_keywords[ctkwidget]:
                    call_argument_remover.add_keyword_removal(ctkwidget, kw)

        tree = call_argument_changer.visit(tree)
        tree = call_argument_remover.visit(tree)
        


        print("Unparsing tree...")  
        status.update("Unparsing tree...")
        try:
            source = ast.unparse(tree)
        except:
            verbose_print("Could not unparse tree")
            raise SyntaxError("Could not unparse tree")
        finally:
            source = source.replace("from customtkinter import \n", "")
            source = source.replace("ctk.CTkMessage(", "tk.Message(")
            source = source.replace("import tkinter as tk", "import tkinter as tk\n")
        
            with open(output_filename, "w", errors="ignore") as f:
                f.write(source)
        
        with open(output_filename, "r", errors="ignore") as f:
            source = f.read()
        
        # remove banned keywords
        lines = source.split("\n")
        new_lines = []
        count = 0
        for line in lines:
            for ctkwidget in ctk_qualified_widget_names:
                if line.find(ctkwidget+"(") != -1:
                    for bannedkw in ctk_cant_have_these_keywords[ctkwidget]:
                        if bannedkw + "=" in line:
                            count+=1
                            line = remove_keyword_from_line(line, bannedkw)
                    break
            
            new_lines.append(line)                

    con.print(f" {count} keyword(s) removed")
            
    source = "\n".join(new_lines)

    con.print(f" {source.count('ctk.CTk')} widgets replaced!")
        
    with open(output_filename, "w") as f:
        f.write(source)

    verbose_print(output_filename)
    verbose_print("done.")


def input_filename_to_output_filename(input_filename: str) -> str:
    return os.path.join(
        os.getcwd(), "customtkinter_" + os.path.basename(str(input_filename))
    )


def main():
    global Gverbose

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        print_warning(" -m/--multiple flag expected at least one argument")
        return

    Gverbose = args.Verbose
    verbose_print("Checking Flags...")

    if args.Examples:
        print_examples()
        return

    if args.Target == None and args.Multiple == []:
        print_help_screen()
        print_warning(" You must specify a target file to convert....")
        return

    if args.Help:
        verbose_print("Help activated...")
        parser.print_help()

    if args.Listboxes:
        verbose_print("Listbox Converter Activated")

    if args.Output != None:
        verbose_print(f"Output file specified: {args.Output}")

    elif args.Output == None and args.Target != None:
        verbose_print("Output not specified, making one from input file")
        args.Output = input_filename_to_output_filename(args.Target)

    if args.Multiple != []:
        verbose_print("Multiple conversions underway...")

        if args.Output != None:
            verbose_print(
                "Multiple flag used with outfile flag, defaulting to name generator..."
            )
            print_warning("Cant specify output file with multiple conversions")

        for index, item in enumerate(args.Multiple):
            verbose_print(f"Conversion {index+1} : {item}")
            if os.path.exists(item):
                output = input_filename_to_output_filename(item)
                make_custom_tkinter(
                    input_file=item,
                    output_filename=output,
                    convert_listboxes=args.Listboxes,
                    verbose=args.Verbose,
                )
                print_update(f"Finished {output}")
            else:
                print_warning(f"Cant locate {item}")
        return
    else:
        verbose_print("Single Target conversion underway...")
        try:
            if os.path.exists(str(args.Target)):
                make_custom_tkinter(
                    input_file=args.Target,
                    output_filename=args.Output,
                    convert_listboxes=args.Listboxes,
                    verbose=args.Verbose,
                )
                fn = args.Output if args.Output != None else args.Target
                print_update(f"Finished {fn}")
                return
        except AttributeError:

            print_help_screen()
            print_warning("Must specify a Target to convert...")
            return

        except FileNotFoundError:

            trypath = os.path.join(os.getcwd(), os.path.basename(str(args.Target)))
            if os.path.exists(trypath):
                make_custom_tkinter(
                    input_file=trypath,
                    output_filename=args.Output,
                    convert_listboxes=args.Listboxes,
                    verbose=args.Verbose,
                )

            else:
                print_warning(f"Could not find file {args.Target}")
                return


if __name__ == "__main__":
    main()
