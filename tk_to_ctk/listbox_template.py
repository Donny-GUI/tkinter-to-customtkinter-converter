"""Embedded CTkListbox helper used for optional listbox conversion."""

from __future__ import annotations

LISTBOX_TEMPLATE = """
class CTkListbox(ctk.CTkScrollableFrame):
    \"\"\"Minimal listbox compatibility wrapper for converted tkinter code.\"\"\"

    def __init__(
        self,
        master,
        height=100,
        width=200,
        fg_color="transparent",
        bg_color=None,
        text_color="default",
        hover_color="default",
        button_fg_color="default",
        border_width=3,
        font="default",
        multiple_selection=False,
        listvariable=None,
        hover=True,
        command=None,
        justify="left",
        **kwargs,
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            fg_color=fg_color,
            border_width=border_width,
            **kwargs,
        )
        self._scrollbar.grid_configure(padx=(0, border_width + 4))
        self._scrollbar.configure(width=12)

        if bg_color is not None:
            super().configure(bg_color=bg_color)

        self.select_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.text_color = (
            ctk.ThemeManager.theme["CTkButton"]["text_color"]
            if text_color == "default"
            else text_color
        )
        self.hover_color = (
            ctk.ThemeManager.theme["CTkButton"]["hover_color"]
            if hover_color == "default"
            else hover_color
        )
        self.font = (
            (ctk.ThemeManager.theme["CTkFont"]["family"], 13)
            if font == "default"
            else font
        )
        self.button_fg_color = (
            "transparent" if button_fg_color == "default" else button_fg_color
        )

        if justify == "left":
            self.justify = "w"
        elif justify == "right":
            self.justify = "e"
        else:
            self.justify = "c"

        self.buttons = {}
        self.command = command
        self.multiple = multiple_selection
        self.selected = None
        self.hover = hover
        self.end_num = 0
        self.selections = []

        if listvariable is not None:
            self.listvariable = listvariable
            self.listvariable.trace_add("write", lambda *_: self.update_listvar())
            self.update_listvar()

    def update_listvar(self):
        values = list(eval(self.listvariable.get()))
        self.delete("all")
        for item in values:
            self.insert("end", item)

    def insert(self, index, option, **kwargs):
        if str(index).lower() == "end":
            index = f"END{self.end_num}"
            self.end_num += 1

        button = ctk.CTkButton(
            self,
            text=option,
            fg_color=self.button_fg_color,
            anchor=self.justify,
            text_color=self.text_color,
            font=self.font,
            hover_color=self.hover_color,
            **kwargs,
        )
        button.configure(command=lambda key=index: self.select(key))
        button.pack(padx=0, pady=(0, 5), fill="x", expand=True)
        self.buttons[index] = button
        return button

    def select(self, index):
        for button in self.buttons.values():
            button.configure(fg_color=self.button_fg_color)

        selected = self.buttons[index]
        if self.multiple:
            if selected in self.selections:
                self.selections.remove(selected)
            else:
                self.selections.append(selected)
            for button in self.selections:
                button.configure(fg_color=self.select_color)
        else:
            self.selected = selected
            selected.configure(fg_color=self.select_color)

        if self.command is not None:
            self.command(self.get())

    def delete(self, index, last=None):
        if str(index).lower() == "all":
            for button in self.buttons.values():
                button.destroy()
            self.buttons = {}
            self.end_num = 0
            return

        if last is not None:
            if str(last).lower() == "end":
                last = len(self.buttons) - 1
            keys = list(self.buttons.keys())[int(index) : int(last) + 1]
            for key in keys:
                self.buttons[key].destroy()
                del self.buttons[key]
            return

        key = list(self.buttons.keys())[int(index)]
        self.buttons[key].destroy()
        del self.buttons[key]

    def get(self, index=None):
        if index is not None:
            if str(index).lower() == "all":
                return [button.cget("text") for button in self.buttons.values()]
            key = list(self.buttons.keys())[int(index)]
            return self.buttons[key].cget("text")

        if self.multiple:
            return [button.cget("text") for button in self.selections]
        return self.selected.cget("text") if self.selected is not None else None

    def curselection(self):
        if self.multiple:
            indexes = []
            for index, button in enumerate(self.buttons.values()):
                if button in self.selections:
                    indexes.append(index)
            return tuple(indexes)

        for index, button in enumerate(self.buttons.values()):
            if button == self.selected:
                return index
        return None

    def size(self):
        return len(self.buttons)

    def configure(self, **kwargs):
        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            for button in self.buttons.values():
                button.configure(hover_color=self.hover_color)
        if "button_fg_color" in kwargs:
            self.button_fg_color = kwargs.pop("button_fg_color")
            for button in self.buttons.values():
                button.configure(fg_color=self.button_fg_color)
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            for button in self.buttons.values():
                button.configure(text_color=self.text_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            for button in self.buttons.values():
                button.configure(font=self.font)
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        super().configure(**kwargs)
""".strip()
