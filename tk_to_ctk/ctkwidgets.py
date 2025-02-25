
from optparse import NO_DEFAULT
from tkinter import NO
from dataclasses import dataclass
from enum import Enum, StrEnum

class ctk(StrEnum):
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

    def list_widget_arguments(widget_name:str) -> list[str]:
        if not widget_name.startswith("ctk."):
            widget_name = "ctk." + widget_name

        if widget_name in ctk_widget_names:
            return ctk_widget_arguments[widget_name]
        else:
            return []
    
    def get_equivalent_widget(widget_name:str) -> str:
        if widget_name.startswith("tk.") or widget_name.startswith("ttk."):
            if widget_name in ctk_widget_names:
                return tk_widget_to_ctk_widget[widget_name]
            else:
                return widget_name
        else:
            widget_name = "tk." + widget_name
            if widget_name in ctk_widget_names:
                return tk_widget_to_ctk_widget[widget_name]
            else:
                widget_name = "ttk." + widget_name.split(".", 1)[1]
                if widget_name in ctk_widget_names:
                    return tk_widget_to_ctk_widget[widget_name]
                else:
                    return widget_name.split(".", 1)[1]
    

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
}

tk_widget_to_ctk_widget = {
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
    "tk.BooleanVar":                ctk.CTkVariable,
    "tk.DoubleVar":                 ctk.CTkVariable,
    "tk.IntVar":                    ctk.CTkVariable,
    "tk.StringVar":                 ctk.CTkVariable,
    "tk.BitmapImage":               ctk.CTkImage,
    "tk.PhotoImage":                ctk.CTkImage,
    "tk.font.Font":                 ctk.CTkFont,
    
    "ttk.Button":                    ctk.CTkButton,
    "ttk.Checkbutton":               ctk.CTkCheckBox,
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
    "ttk."
}


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


for widget in ctk_widget_arguments.keys():
    print(str(widget[4:].ljust(20)) + " = '" + str(widget[4:]) + "'")
    