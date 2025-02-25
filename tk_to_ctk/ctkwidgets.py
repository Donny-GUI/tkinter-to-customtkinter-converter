
from multiprocessing.spawn import import_main_path
from optparse import NO_DEFAULT
from tkinter import NO
from dataclasses import dataclass
from enum import Enum, StrEnum


CTkButton            = 'CTkButton'
CTk                  = 'CTk'
CTkInputDialog       = 'CTkInputDialog'
CTkToplevel          = 'CTkToplevel'
CTkCheckBox          = 'CTkCheckBox'
CTkComboBox          = 'CTkComboBox'
CTkEntry             = 'CTkEntry'
CTkFrame             = 'CTkFrame'
CTkLabel             = 'CTkLabel'
CTkOptionMenu        = 'CTkOptionMenu'
CTkProgressBar       = 'CTkProgressBar'
CTkRadioButton       = 'CTkRadioButton'
CTkScrollableFrame   = 'CTkScrollableFrame'
CTkScrollbar         = 'CTkScrollbar'
CTkSegmentedButton   = 'CTkSegmentedButton'
CTkSlider            = 'CTkSlider'
CTkSwitch            = 'CTkSwitch'
CTkTabview           = 'CTkTabview'
CTkFrames            = 'CTkFrames'
CTkTextbox           = 'CTkTextbox'
CTkFont              = 'CTkFont'
CTkImage             = 'CTkImage'

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


class ctk:
    CTkButton            = 'ctk.CTkButton'
    CTk                  = 'ctk.CTk'
    CTkInputDialog       = 'ctk.CTkInputDialog'
    CTkToplevel          = 'ctk.CTkToplevel'
    CTkCheckBox          = 'ctk.CTkCheckBox'
    CTkComboBox          = 'ctk.CTkComboBox'
    CTkEntry             = 'ctk.CTkEntry'
    CTkFrame             = 'ctk.CTkFrame'
    CTkLabel             = 'ctk.CTkLabel'
    CTkOptionMenu        = 'ctk.CTkOptionMenu'
    CTkProgressBar       = 'ctk.CTkProgressBar'
    CTkRadioButton       = 'ctk.CTkRadioButton'
    CTkScrollableFrame   = 'ctk.CTkScrollableFrame'
    CTkScrollbar         = 'ctk.CTkScrollbar'
    CTkSegmentedButton   = 'ctk.CTkSegmentedButton'
    CTkSlider            = 'ctk.CTkSlider'
    CTkSwitch            = 'ctk.CTkSwitch'
    CTkTabview           = 'ctk.CTkTabview'
    CTkFrames            = 'ctk.CTkFrames'
    CTkTextbox           = 'ctk.CTkTextbox'
    CTkFont              = 'ctk.CTkFont'
    CTkImage             = 'ctk.CTkImage'
    CTkVariable          = 'ctk.CTkVariable'
    CTkCanvas            = 'ctk.CTkCanvas'
    CTkIntVar            = 'ctk.CTkIntVar'
    CTkDoubleVar         = 'ctk.CTkDoubleVar'
    CTkStringVar         = 'ctk.CTkStringVar'
    CTkBooleanVar        = 'ctk.CTkBooleanVar'
    CTkPhotoImage        = 'ctk.CTkPhotoImage'


REMOVE = 333

class CTkWidgets(ctk):
    def __init__(self):
        super().__init__()
        self._ctk_members = [self.CTkButton, self.CTk, self.CTkInputDialog, self.CTkToplevel, self.CTkCheckBox, self.CTkComboBox, self.CTkEntry, self.CTkFrame, self.CTkLabel, self.CTkOptionMenu, self.CTkProgressBar, self.CTkRadioButton, self.CTkScrollableFrame, self.CTkScrollbar, self.CTkSegmentedButton, self.CTkSlider, self.CTkSwitch, self.CTkTabview, self.CTkFrames, self.CTkTextbox, self.CTkFont, self.CTkImage, self.CTkVariable, self.CTkCanvas, self.CTkIntVar, self.CTkDoubleVar, self.CTkStringVar, self.CTkBooleanVar, self.CTkPhotoImage]
        self._ctk_names = self._ctk_members + ctk_widget_names
        self._ctk_widgets = ctk_widget_names
        self._ctk_arguments = ctk_widget_arguments
        self._tk_arguments = tk_widget_arguments
        self._tk2ctk_map = tk_widget_to_ctk_widget
        self._tk_names = tk_widgets
        self._tk_keywords_to_ctk = {
            "orient": "orientation",
            "borderwidth": "border_width",
            
        }
    def match(self, name:str) -> str:
        if name in self._tk_names:
            return self._tk2ctk_map[name]
        else:
            return name
        
    def match_args(self, name:str) -> list[str]:
        if name in self._ctk_names:
            return self._ctk_arguments[name]
        elif name in self._tk_names:
            return tk_widget_arguments[name]
        else:
            return []
    
    def is_ctk(self, name:str) -> bool:
        return name in self._ctk_names
    
    def is_tk(self, name:str) -> bool:
        return name in self._tk_names
        

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

universal_kw_translation = {
    "background": "bg_color",
    "foreground": "fg_color",
    "fg": "fg_color",
    "orient": "orientation",
    "bg": "bg_color",
    "borderwidth": "border_width",
    "text_variable": "textvariable",
    "from": "from_",
    "labelanchor": "label_anchor"
}

tk_widget_to_ctk_widget = {
    "tk.Tk":                        ctk.CTk,
    "tk.Canvas":                    ctk.CTkCanvas,
    "tk.ButtonBox":                 ctk.CTkSegmentedButton,
    "tk.Button":                    ctk.CTkButton,
    "tk.Checkbutton":               ctk.CTkCheckBox,
    "tk.Entry":                     ctk.CTkEntry,
    "tk.Frame":                     ctk.CTkFrame,
    "tk.Label":                     ctk.CTkLabel,
    "tk.LabelFrame":                ctk.CTkScrollableFrame,
    "tk.Menu":                      ctk.CTkOptionMenu,
    "tk.OptionMenu":                ctk.CTkOptionMenu,
    "tk.Panedwindow":               ctk.CTkTabview,
    "tk.Progressbar":               ctk.CTkProgressBar,
    "tk.Radiobutton":               ctk.CTkRadioButton,
    "tk.Scale":                     ctk.CTkSlider,
    "tk.Scrollbar":                 ctk.CTkScrollbar,
    #"tk.Spinbox":                   ctk.CTkSpinbox,
    "tk.Text":                      ctk.CTkTextbox,
    "tk.Toplevel":                  ctk.CTkToplevel,
    "tk.Variable":                  ctk.CTkVariable,
    "tk.BooleanVar":                ctk.CTkBooleanVar,
    "tk.DoubleVar":                 ctk.CTkDoubleVar,
    "tk.IntVar":                    ctk.CTkIntVar,
    "tk.StringVar":                 ctk.CTkStringVar,
    "tk.BitmapImage":               ctk.CTkImage,
    "tk.PhotoImage":                ctk.CTkPhotoImage,
    "tk.font.Font":                 ctk.CTkFont,
    
    "ttk.Button":                    ctk.CTkButton,
    "ttk.Menubutton":                ctk.CTkButton,
    "ttk.LabeledScale":              ctk.CTkSlider,
    "ttk.Labelframe":                ctk.CTkScrollableFrame,
    "ttk.Checkbutton":               ctk.CTkCheckBox,
    "ttk.Checkbox":                  ctk.CTkCheckBox,
    "ttk.Combobox":                  ctk.CTkComboBox,
    "ttk.Entry":                     ctk.CTkEntry,
    "ttk.Frame":                     ctk.CTkFrame,
    "ttk.Label":                     ctk.CTkLabel,
    "ttk.LabelFrame":                ctk.CTkScrollableFrame,
    "ttk.Menu":                      ctk.CTkOptionMenu,
    "ttk.OptionMenu":                ctk.CTkOptionMenu,
    "ttk.Panedwindow":               ctk.CTkTabview,
    "ttk.Progressbar":               ctk.CTkProgressBar,
    "ttk.Radiobutton":               ctk.CTkRadioButton,
    "ttk.Scale":                     ctk.CTkSlider,
    "ttk.Scrollbar":                 ctk.CTkScrollbar,
    #"tk.Spinbox":                   ctk.CTkSpinbox,
    "ttk.Text":                      ctk.CTkTextbox,
    "ttk.Toplevel":                  ctk.CTkToplevel,
    "ttk.Variable":                  ctk.CTkVariable,
    "ttk.BooleanVar":                ctk.CTkVariable,
    "ttk.DoubleVar":                 ctk.CTkVariable,
    "ttk.IntVar":                    ctk.CTkVariable,
    "ttk.StringVar":                 ctk.CTkVariable,
    "ttk.BitmapImage":               ctk.CTkImage,
    "ttk.PhotoImage":                ctk.CTkImage,
    "ttk.font.Font":                 ctk.CTkFont,
    "ttk.Notebook":                  ctk.CTkTabview,
}

def match_tk(tk:str):
    return tk_widget_to_ctk_widget.get(tk, None)

def replace_tk(tk:str):
    return tk_widget_to_ctk_widget.get(tk, tk)
    

tk_widgets = [
    "tk.Tk",
    "tk.Button",
    "tk.Canvas",
    "tk.Checkbutton",
    "tk.Entry",
    "tk.Frame",
    "tk.Label",
    "tk.LabelFrame",
    "tk.Listbox",
    "tk.Menu",
    "tk.Menubutton",
    "tk.Message",
    "tk.OptionMenu",
    "tk.Panedwindow",
    "tk.Progressbar",
    "tk.Radiobutton",
    "tk.Scale",
    "tk.Scrollbar",
    "tk.Separator",
    "tk.Spinbox",
    "tk.Text",
    "tk.Toplevel",
    "tk.Treeview",
    "tk.Variable",
    "tk.BooleanVar",
    "tk.DoubleVar",
    "tk.IntVar",
    "tk.StringVar",
    "tk.BitmapImage",
    "tk.PhotoImage",
    "tk.filedialog.Directory",
    "tk.filedialog.Open",
    "tk.filedialog.SaveAs",
    "tk.colorchooser.Chooser",
    "tk.font.Font",
    "tk.ttk.Style"
    # TTK ---------------------------------------
    "ttk.Button",
    "ttk.Checkbutton",
    "ttk.Combobox",
    "ttk.Entry",
    "ttk.Frame",
    "ttk.Label",
    "ttk.LabeledScale",
    "ttk.Labelframe",
    "ttk.Menubutton",
    "ttk.Notebook",
    "ttk.OptionMenu",
    "ttk.Panedwindow",
    "ttk.Progressbar",
    "ttk.Radiobutton",
    "ttk.Scale",
    "ttk.Scrollbar",
    "ttk.Separator",
    "ttk.Sizegrip",
    "ttk.Spinbox",
    "ttk.Treeview",
    'Tk', 'Button', 'Canvas', 'Checkbutton', 'Entry', 'Frame', 'Label', 'LabelFrame', 'Listbox', 'Menu', 'Menubutton', 'Message', 'OptionMenu', 'Panedwindow', 'Progressbar', 'Radiobutton', 'Scale', 'Scrollbar', 'Separator', 'Spinbox', 'Text', 'Toplevel', 'Treeview', 'Variable', 'BooleanVar', 'DoubleVar', 'IntVar', 'StringVar', 'BitmapImage', 'PhotoImage', 'filedialog.Directory', 'filedialog.Open', 'filedialog.SaveAs', 'colorchooser.Chooser', 'font.Font', 'ttk.Stylettk.Button', 'Checkbutton', 'Combobox', 'Entry', 'Frame', 'Label', 'LabeledScale', 'Labelframe', 'Menubutton', 'Notebook', 'OptionMenu', 'Panedwindow', 'Progressbar', 'Radiobutton', 'Scale', 'Scrollbar', 'Separator', 'Sizegrip', 'Spinbox', 'Treeview',
]

tk_available_events = [
    "<Activate>",
    "<Deactivate>",
    "<MouseWheel>",
    "<KeyPress>",
    "<KeyRelease>",
    "<ButtonPress>",
    "<ButtonRelease>",
    "<Motion>",
    "<Configure>",
    "<Destroy>",
    "<FocusIn>",
    "<FocusOut>",
    "<Enter>",
    "<Leave>",
]

def test_to_see_by_name_which_ctk_widgets_lose_kws():
    import json 
    data = {}
    for tk_widget, tk_args in tk_widget_arguments.items():
        ctk_widget = match_tk(tk_widget)
        if ctk_widget is None:
            continue
        data[ctk_widget] = []
        ctk_args = ctk_widget_arguments[ctk_widget]
        for arg in tk_args:
            if arg not in ctk_args:
                if arg in universal_kw_translation:
                    continue
                data[ctk_widget].append(arg)
    from pprint import pprint 
    pprint(data)
                

def test_to_find_bisected_keywords():

    def letters_percentage(string:str, string2:str):
        return len([x for x in string if x in string2]) / len(string)
    

    def normalize(string:str):
        return string.replace("_", "")
    
    for tk_widget, tk_args in tk_widget_arguments.items():
        
        ctk_widget = match_tk(tk_widget)
        if ctk_widget is None:
            continue
        ctk_args = ctk_widget_arguments[ctk_widget]

        
        for arg in tk_args:
            current_match = ""
            highest = 0.0
            for ctk_arg in ctk_args:
                if arg == ctk_arg:
                    break
                percent = letters_percentage(arg, ctk_arg)
                if percent > highest:
                    highest = percent
                    current_match = ctk_arg
            else:
                continue
            print("possible match tk -> ctk: " + arg + " -> " + current_match, highest)    

        norm_tk_args = [normalize(x) for x in tk_args]
        norm_ctk_args = [normalize(x) for x in ctk_args]

        for index, norm_ctk_arg in enumerate(norm_ctk_args):

            if norm_ctk_arg in norm_tk_args:
                c = ctk_args[index]
                n = tk_args[norm_tk_args.index(norm_ctk_arg)]
                
                print(ctk_widget + " : " + c + " <- " + n)






def test_to_see_what_keywords_dont_translate_at_all():

    def letters_percentage(string:str, string2:str):
        return len([x for x in string if x in string2]) / len(string)
    
    ctks = []
    for ctk_widget, ctk_args in ctk_widget_arguments.items():
        ctks.extend(ctk_args)
    ctks = set(ctks)

    percents = []
    tks = set()
    for tk_widget, tk_args in tk_widget_arguments.items():
        for tk_arg in tk_args:
            if tk_arg not in ctks:
                if tk_arg in tks:
                    continue
                tks.add(tk_arg)
    
    for index, tk in enumerate(tks):
        print(tk)
    

