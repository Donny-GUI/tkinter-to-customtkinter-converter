"""Realistic Tkinter app fixture for batch and reviewability tests."""

import tkinter as tk
from tkinter import ttk


# Top-level helper comment should survive conversion.
class DemoFrame(tk.Frame):
    def __init__(self, master, status_var: tk.StringVar):
        super().__init__(master, bg="white")
        self.status_var = status_var

        # Multiline constructor with a nested callback.
        self.header = tk.Label(
            self,
            text="Dashboard",
            fg="navy",
            bg="white",
        )
        self.header.pack(pady=8)

        self.progress = ttk.Progressbar(
            self,
            value=25,
            maximum=100,
        )
        self.progress.pack(fill="x", padx=8)

        self.menu = tk.OptionMenu(
            self,
            self.status_var,
            "Ready",
            "Running",
            "Paused",
            command=lambda value: self._log_change(value),
        )
        self.menu.pack()

        self.scale = tk.Scale(
            self,
            from_=0,
            to=10,
            resolution=1,
            orient=tk.HORIZONTAL,
        )
        self.scale.pack()

        self.canvas = tk.Canvas(self, width=100, height=40)
        self.canvas.pack()

    def _log_change(self, value: str) -> None:
        print("changed", value)


def build_footer(parent: tk.Misc) -> tk.Button:
    # Builder comments should remain readable.
    button = tk.Button(
        parent,
        text="Close",
        command=lambda: parent.winfo_toplevel().destroy(),
    )
    button.configure(fg="white", bg="black")
    return button


class DemoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Realistic Fixture")
        self.status_var = tk.StringVar(value="Ready")

        frame = DemoFrame(self, self.status_var)
        frame.grid(row=0, column=0, sticky="nsew")

        footer = build_footer(self)
        footer.pack(pady=12)
