"""Explicit widget and option mappings for the converter."""

from __future__ import annotations

from .models import OptionRule, WidgetRule


def rename(name: str) -> OptionRule:
    """Create a simple rename rule."""

    return OptionRule(rename_to=name)


def drop(note: str) -> OptionRule:
    """Create an option-drop rule with an explanation."""

    return OptionRule(drop=True, note=note)


def build_rule(
    source_name: str,
    target_name: str | None,
    *,
    category: str = "direct",
    options: dict[str, OptionRule] | None = None,
    allowed: set[str] | None = None,
    unsupported_reason: str | None = None,
) -> WidgetRule:
    """Build a widget rule with immutable option metadata."""

    return WidgetRule(
        source_name=source_name,
        target_name=target_name,
        category=category,
        option_rules=options or {},
        allowed_options=frozenset(allowed or set()),
        unsupported_reason=unsupported_reason,
    )


WINDOW_ALLOWED = {"fg_color"}
FRAME_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_width",
    "bg_color",
    "fg_color",
    "border_color",
}
LABEL_ALLOWED = {
    "text",
    "textvariable",
    "width",
    "height",
    "corner_radius",
    "fg_color",
    "text_color",
    "font",
    "anchor",
    "compound",
    "padx",
    "pady",
    "wraplength",
}
BUTTON_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_width",
    "border_spacing",
    "fg_color",
    "hover_color",
    "border_color",
    "text_color",
    "text_color_disabled",
    "text",
    "font",
    "textvariable",
    "image",
    "state",
    "hover",
    "command",
    "compound",
    "anchor",
}
ENTRY_ALLOWED = {
    "textvariable",
    "width",
    "height",
    "corner_radius",
    "fg_color",
    "border_color",
    "text_color",
    "placeholder_text_color",
    "placeholder_text",
    "font",
    "state",
}
CHECKBOX_ALLOWED = {
    "width",
    "height",
    "checkbox_width",
    "checkbox_height",
    "corner_radius",
    "border_width",
    "fg_color",
    "border_color",
    "hover_color",
    "checkmark_color",
    "text_color",
    "text",
    "textvariable",
    "font",
    "hover",
    "state",
    "variable",
    "onvalue",
    "offvalue",
    "command",
}
RADIO_ALLOWED = {
    "width",
    "height",
    "radiobutton_width",
    "radiobutton_height",
    "corner_radius",
    "border_width_checked",
    "border_width_unchecked",
    "fg_color",
    "border_color",
    "hover_color",
    "text_color",
    "text",
    "textvariable",
    "font",
    "hover",
    "state",
    "variable",
    "value",
    "command",
}
COMBOBOX_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_width",
    "fg_color",
    "border_color",
    "button_color",
    "button_hover_color",
    "dropdown_fg_color",
    "dropdown_hover_color",
    "dropdown_text_color",
    "text_color",
    "font",
    "dropdown_font",
    "values",
    "variable",
    "state",
    "hover",
    "command",
}
TEXTBOX_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_width",
    "border_spacing",
    "fg_color",
    "border_color",
    "text_color",
    "scrollbar_button_color",
    "scrollbar_button_hover_color",
    "font",
    "state",
    "wrap",
}
SCROLLBAR_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_spacing",
    "fg_color",
    "button_color",
    "button_hover_color",
    "hover",
    "orientation",
    "command",
}
SLIDER_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "button_corner_radius",
    "border_width",
    "button_length",
    "fg_color",
    "progress_color",
    "button_color",
    "button_hover_color",
    "border_color",
    "from_",
    "to",
    "state",
    "number_of_steps",
    "hover",
    "command",
    "orientation",
    "variable",
}
OPTIONMENU_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "fg_color",
    "button_color",
    "button_hover_color",
    "text_color",
    "text_color_disabled",
    "dropdown_fg_color",
    "dropdown_hover_color",
    "dropdown_text_color",
    "font",
    "dropdown_font",
    "values",
    "variable",
    "command",
    "state",
    "hover",
    "anchor",
    "dynamic_resizing",
}
PROGRESS_ALLOWED = {
    "width",
    "height",
    "corner_radius",
    "border_width",
    "fg_color",
    "border_color",
    "progress_color",
    "mode",
    "determinate_speed",
    "indeterminate_speed",
    "orientation",
}
TOPLEVEL_ALLOWED = {"fg_color"}


COMMON_SURFACE_OPTIONS = {
    "bg": rename("fg_color"),
    "background": rename("fg_color"),
    "bd": rename("border_width"),
    "borderwidth": rename("border_width"),
}
TEXT_COLOR_OPTIONS = {
    "fg": rename("text_color"),
    "foreground": rename("text_color"),
}


WIDGET_RULES: dict[str, WidgetRule] = {
    "tk.Tk": build_rule(
        "tk.Tk",
        "ctk.CTk",
        options={"bg": rename("fg_color"), "background": rename("fg_color")},
        allowed=WINDOW_ALLOWED,
    ),
    "tk.Toplevel": build_rule(
        "tk.Toplevel",
        "ctk.CTkToplevel",
        options={"bg": rename("fg_color"), "background": rename("fg_color")},
        allowed=TOPLEVEL_ALLOWED,
    ),
    "tk.Frame": build_rule(
        "tk.Frame",
        "ctk.CTkFrame",
        options=COMMON_SURFACE_OPTIONS,
        allowed=FRAME_ALLOWED,
    ),
    "ttk.Frame": build_rule(
        "ttk.Frame",
        "ctk.CTkFrame",
        allowed=FRAME_ALLOWED,
    ),
    "tk.Label": build_rule(
        "tk.Label",
        "ctk.CTkLabel",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=LABEL_ALLOWED,
    ),
    "ttk.Label": build_rule(
        "ttk.Label",
        "ctk.CTkLabel",
        options=TEXT_COLOR_OPTIONS,
        allowed=LABEL_ALLOWED,
    ),
    "tk.Button": build_rule(
        "tk.Button",
        "ctk.CTkButton",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=BUTTON_ALLOWED,
    ),
    "ttk.Button": build_rule(
        "ttk.Button",
        "ctk.CTkButton",
        options=TEXT_COLOR_OPTIONS,
        allowed=BUTTON_ALLOWED,
    ),
    "tk.Entry": build_rule(
        "tk.Entry",
        "ctk.CTkEntry",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=ENTRY_ALLOWED,
    ),
    "ttk.Entry": build_rule(
        "ttk.Entry",
        "ctk.CTkEntry",
        options=TEXT_COLOR_OPTIONS,
        allowed=ENTRY_ALLOWED,
    ),
    "tk.Checkbutton": build_rule(
        "tk.Checkbutton",
        "ctk.CTkCheckBox",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=CHECKBOX_ALLOWED,
    ),
    "ttk.Checkbutton": build_rule(
        "ttk.Checkbutton",
        "ctk.CTkCheckBox",
        options=TEXT_COLOR_OPTIONS,
        allowed=CHECKBOX_ALLOWED,
    ),
    "ttk.Checkbox": build_rule(
        "ttk.Checkbox",
        "ctk.CTkCheckBox",
        options=TEXT_COLOR_OPTIONS,
        allowed=CHECKBOX_ALLOWED,
    ),
    "tk.Radiobutton": build_rule(
        "tk.Radiobutton",
        "ctk.CTkRadioButton",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=RADIO_ALLOWED,
    ),
    "ttk.Radiobutton": build_rule(
        "ttk.Radiobutton",
        "ctk.CTkRadioButton",
        options=TEXT_COLOR_OPTIONS,
        allowed=RADIO_ALLOWED,
    ),
    "tk.Scrollbar": build_rule(
        "tk.Scrollbar",
        "ctk.CTkScrollbar",
        options=COMMON_SURFACE_OPTIONS | {"orient": rename("orientation")},
        allowed=SCROLLBAR_ALLOWED,
    ),
    "ttk.Scrollbar": build_rule(
        "ttk.Scrollbar",
        "ctk.CTkScrollbar",
        options={"orient": rename("orientation")},
        allowed=SCROLLBAR_ALLOWED,
    ),
    "tk.Text": build_rule(
        "tk.Text",
        "ctk.CTkTextbox",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        allowed=TEXTBOX_ALLOWED,
    ),
    "ttk.Combobox": build_rule(
        "ttk.Combobox",
        "ctk.CTkComboBox",
        options=TEXT_COLOR_OPTIONS | {"textvariable": rename("variable")},
        allowed=COMBOBOX_ALLOWED,
        category="direct",
    ),
    "tk.Scale": build_rule(
        "tk.Scale",
        "ctk.CTkSlider",
        options=COMMON_SURFACE_OPTIONS | {"orient": rename("orientation")},
        allowed=SLIDER_ALLOWED,
        category="special",
    ),
    "ttk.Scale": build_rule(
        "ttk.Scale",
        "ctk.CTkSlider",
        options={"orient": rename("orientation")},
        allowed=SLIDER_ALLOWED,
        category="special",
    ),
    "tk.OptionMenu": build_rule(
        "tk.OptionMenu",
        "ctk.CTkOptionMenu",
        allowed=OPTIONMENU_ALLOWED,
        category="special",
    ),
    "ttk.Progressbar": build_rule(
        "ttk.Progressbar",
        "ctk.CTkProgressBar",
        options={"orient": rename("orientation")},
        allowed=PROGRESS_ALLOWED,
        category="special",
    ),
    "tk.Listbox": build_rule(
        "tk.Listbox",
        "CTkListbox",
        options=COMMON_SURFACE_OPTIONS | TEXT_COLOR_OPTIONS,
        category="special",
    ),
    "tk.Canvas": build_rule(
        "tk.Canvas",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Canvas replacement.",
    ),
    "tk.Menu": build_rule(
        "tk.Menu",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Menu replacement.",
    ),
    "tk.Menubutton": build_rule(
        "tk.Menubutton",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Menubutton replacement.",
    ),
    "tk.Message": build_rule(
        "tk.Message",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Message replacement.",
    ),
    "tk.PanedWindow": build_rule(
        "tk.PanedWindow",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct PanedWindow replacement.",
    ),
    "tk.LabelFrame": build_rule(
        "tk.LabelFrame",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct LabelFrame replacement.",
    ),
    "ttk.Treeview": build_rule(
        "ttk.Treeview",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Treeview replacement.",
    ),
    "ttk.Separator": build_rule(
        "ttk.Separator",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Separator replacement.",
    ),
    "ttk.Notebook": build_rule(
        "ttk.Notebook",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Notebook replacement.",
    ),
    "ttk.Panedwindow": build_rule(
        "ttk.Panedwindow",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Panedwindow replacement.",
    ),
    "ttk.Labelframe": build_rule(
        "ttk.Labelframe",
        None,
        category="unsupported",
        unsupported_reason="CustomTkinter has no direct Labelframe replacement.",
    ),
}


TK_VARIABLE_NAMES = {
    "Variable",
    "StringVar",
    "IntVar",
    "BooleanVar",
    "DoubleVar",
    "PhotoImage",
    "BitmapImage",
    "END",
    "HORIZONTAL",
    "VERTICAL",
    "LEFT",
    "RIGHT",
    "TOP",
    "BOTTOM",
    "BOTH",
    "X",
    "Y",
    "N",
    "S",
    "E",
    "W",
    "NW",
    "NE",
    "SW",
    "SE",
    "NSEW",
    "EW",
    "NS",
    "CENTER",
    "WORD",
    "NONE",
    "DISABLED",
    "NORMAL",
    "END",
    "SINGLE",
    "BROWSE",
    "MULTIPLE",
    "EXTENDED",
}


TK_MODULE_NAMES = {"filedialog", "colorchooser", "messagebox"}


def get_widget_rule(source_name: str) -> WidgetRule | None:
    """Return the widget rule for a normalized tkinter name."""

    return WIDGET_RULES.get(source_name)
