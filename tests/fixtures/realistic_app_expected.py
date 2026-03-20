"""Realistic Tkinter app fixture for batch and reviewability tests."""
import customtkinter as ctk
import tkinter as tk


# Top-level helper comment should survive conversion.
class DemoFrame(ctk.CTkFrame):
    def __init__(self, master, status_var: tk.StringVar):
        super().__init__(master, fg_color="white")
        self.status_var = status_var

        # Multiline constructor with a nested callback.
        self.header = ctk.CTkLabel(
            self,
            text="Dashboard",
            text_color="navy",
            fg_color="white")
        self.header.pack(pady=8)

        self.progress = ctk.CTkProgressBar(
            self)
        self.progress.set(0.25)
        self.progress.pack(fill="x", padx=8)

        self.menu = ctk.CTkOptionMenu(
            self,
            variable = self.status_var, values = ["Ready", "Running", "Paused"], command=lambda value: self._log_change(value))
        self.menu.set("Ready")
        self.menu.pack()

        self.scale = ctk.CTkSlider(
            self,
            from_=0,
            to=10,
            orientation=tk.HORIZONTAL, number_of_steps = 10)
        self.scale.pack()
        # TODO tk2ctk: CustomTkinter has no direct Canvas replacement.

        self.canvas = tk.Canvas(self, width=100, height=40)
        self.canvas.pack()

    def _log_change(self, value: str) -> None:
        print("changed", value)


def build_footer(parent: tk.Misc) -> ctk.CTkButton:
    # Builder comments should remain readable.
    button = ctk.CTkButton(
        parent,
        text="Close",
        command=lambda: parent.winfo_toplevel().destroy())
    button.configure(text_color="white", fg_color="black")
    return button


class DemoApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Realistic Fixture")
        self.status_var = tk.StringVar(value="Ready")

        frame = DemoFrame(self, self.status_var)
        frame.grid(row=0, column=0, sticky="nsew")

        footer = build_footer(self)
        footer.pack(pady=12)
