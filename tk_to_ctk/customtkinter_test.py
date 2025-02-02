import customtkinter as ctk
from customtkinter import E, END, LEFT, N, S
import tkinter as tk
from tkinter import filedialog
import subprocess
from .widget_replacer import WidgetReplacer
from .lists import tkinter_widgets, ctk_widgets
import re


current_file = None

def search_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[('Python files', '*.py')])
    if file_path:
        current_file = file_path
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, content)

def convert_file():
    file_content = text_box.get(1.0, tk.END)
    wr = WidgetReplacer(current_file, "temp")
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
    for widg in tkinter_widgets:
        widget: str = "ttk." + widg
        ctk_widget: str = f"ctk.CTk{widg}"
        wr.add_findable("{0}(".format(widget), "{0}(".format(ctk_widget))
        wr.add_findable("{0}, ".format(widget), "")
        wr.add_findable(widget + ",", "{0},".format(ctk_widget))
        wr.add_findable(" = {0}(".format(widget), " = {0}(".format(ctk_widget))
        wr.add_findable("={0}(".format(widget), "={0}(".format(ctk_widget))
        wr.add_findable(": {0} ".format(widget), ": {0} ".format(ctk_widget))
        wr.add_findable(":{0},".format(widget), ":{0},".format(ctk_widget))
        wr.add_findable(":{0}".format(widget), ":{0}".format(ctk_widget))
    wr.replace_widgets()
    wr.double_check()
    content: str = file_content
    cont1: str = re.sub(r"\.config\(", ".configure(", content)
    cont2 = cont1.replace(", bg=", ", bg_color=").replace(", bg =", ", bg_color =")
    cont3 = cont2.replace(", fg=", ", fg_color=").replace(", fg =", ", fg_color =")
    cont4 = cont3.replace(r"(tk.Tk):", r"(ctk.CTk):")
    for index, widget in enumerate(tkinter_widgets):
        cont4 = cont4.replace(f"(tk.{widget}):", f"(ctk.{ctk_widgets[index]}):")
    cont4 = cont4.replace("(Tk):", "(ctk.CTk):")
    cont5 = cont4.replace("Tk()", "ctk.CTk()")

    print('Converted file content:')
    print(file_content)


root = ctk.CTk()
root.title('Python File Converter')
button_frame = ctk.CTkFrame(root, width=600, height=600)
button_frame.pack(pady=10)
search_button = ctk.CTkButton(button_frame, text='Search File', command=search_file)
search_button.pack(side=tk.LEFT, padx=5)
convert_button = ctk.CTkButton(button_frame, text='Convert File', command=convert_file)
convert_button.pack(side=tk.LEFT, padx=5)
text_box = ctk.CTkTextbox(root, wrap='word', width=600, height=400)
text_box.pack(pady=10)
root.mainloop()