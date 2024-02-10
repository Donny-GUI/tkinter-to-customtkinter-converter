import re
import os
import sys
import subprocess
from util import pip_str, python_str
from util import get_listbox_source, has_listbox, classes_begin_index
try:
    from rich.status import Status
except:
    print(f"rich is not installed. Installing...")
    subprocess.run([pip_str, "install", "rich"], check=True)
    print(f"rich has been installed.")
from rich.status import Status
from rich.console import Console
from rich.panel import Panel
from widget_replacer import WidgetReplacer


tkinter_widgets = [
    "Button", "Canvas", "Checkbutton", "Entry", "Label",
    "Menubutton", "Message",  "Radiobutton",
    "Scale", "Scrollbar", "Text", "Toplevel",  "Treeview",
    "Frame", "Progressbar", "Separator"]
ctk_widgets = ["CTk"+x for x in tkinter_widgets]


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

def replace_meta_in_file(file_path: str) -> None:
    """ 
    Replace all the tk meta class or base classes with custom tkinter ones 
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    cont = content.replace(r"(tk.Tk):", r"(ctk.CTk):")
    for index, widget in enumerate(tkinter_widgets):
        cont = cont.replace(f"(tk.{widget}):",f"(ctk.{ctk_widgets[index]}):")
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
    """ 
    Find errors in the tk-ctk psuedo code 
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        retv = []

        for line in lines:
            l = re.sub(r'ttk.ctk.', r'ctk.', line)
            l2 = re.sub(r'tk.ctk.', r'ctk.', l)
            l3 = re.sub(r'.CTkText', r'.CTkTextbox', l2)
            l4 = re.sub(r'.CTkRadiobutton', r'.CTkRadioButton', l3)
            #CTkCheckButton
            l5 = re.sub(r'.CTkCheckbutton', r'.CTkCheckBox', l4)
            l6 = re.sub(r'.CTkScale', r'.CTkSlider', l5)
            #tk.StringVar
            l7 = l6
            retv.append(l7)

    with open(file_path, "w", encoding="utf-8") as wfile:
        for l in retv:
            wfile.write(l)

def rewrite_listboxes(filepath: str) -> None:

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
        content1 = re.sub(r"ttk.Listbox(", r"CTkListbox(", content)
        content2 = re.sub(r"tk.Listbox(", r"CTkListbox(", content1)
        # write the final content
        with open(filepath, "w") as w:
            w.write(content2)

def make_custom_tkinter(input_file:str, output_filename: str, convert_listboxes: bool=False) -> None:
    """
    Description: 
        Create a customtkinter file from a tkinter file
    
    Arguments:
        input_file (str): the tkinter file to use
        output_filename (str): the desired output file
    Returns:
        None

    """
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
        
        find_errs(file_path = output_filename)
        print("Success!")

        if convert_listboxes:
            status.update(" fixing the listboxes...")
            console.print("    Converting listboxes...")
            rewrite_listboxes(file_path = output_filename)

        print(output_filename)


use_panel_str = f"""
  Usage:
    [italic][dim]{python_str} {os.path.basename(__file__)} <[italic][white][dim]Target1> <Target2> ... [/italic][/dim][/white][/italic][/dim]

  Description:
    [italic]Convert your tkinter scripts to customtkinter scripts.[/italic]

  Options:
    help     -h  --help         Show this help
    listbox  -l  --listbox      Convert tkinter listboxes to customtkinter
    outfile  -o  --outfile      Give then name of the outfile

"""


class AppArgs(object):
    def __init__(self) -> None:
        self.arg_len = len(sys.argv)
        self.help_flag = False
        self.listbox_flag = False
        self.outfile_flag = False

        self.outfile_value = None
        self.arg_iter = iter(sys.argv)
        self.targets = []

        for i in range(self.arg_len):

            try:
                nextarg = next(self.arg_iter)
            except StopIteration:
                break

            if nextarg in ["help", "--help", "-h"]:
                self.help_flag = True
            elif nextarg in ["listbox", "--listbox", "-l"]:
                self.listbox_flag = True
            elif nextarg in ["outfile", "--outfile", "-o"]:

                self.outfile_flag = True
                try:
                    nextarg = next(self.arg_iter)
                    self.outfile_value = nextarg
                except StopIteration:
                    break
            elif nextarg not in ["python3", "python", os.path.basename(__file__)] and nextarg.endswith(".py"):
                self.targets.append(nextarg)
        
        if self.outfile_flag == True:
            self.outfile_value = self.outfile_value.rstrip(".py")
            self.outfile_value += ".py"
    
    @property 
    def not_enough(self) -> bool:
        if self.arg_len < 2:
            return True
        return False
    
    @property 
    def has_targets(self) -> bool:
        if self.targets != []:
            return True
        return False

    @property 
    def has_outfile(self) -> bool:
        return self.outfile_flag
    
    @property
    def needs_outfile(self) -> bool:
        if self.outfile_flag and self.outfile_value == None:
            return True
        elif self.outfile_flag and self.outfile_value != None:
            return False
        elif self.outfile_flag == False:
            return False
    
    @property 
    def multitarget(self) -> bool:
        return True if len(self.targets) > 1 else False
    
    @property
    def singletarget(self) -> bool:
        return True if len(self.targets) == 1 else False
    

if __name__ == "__main__":
    
    console = Console()
    args = AppArgs()

    if args.not_enough:
        console.print(Panel(use_panel_str, highlight="blue", title="[blue]Tkinter to CustomTkinter[/blue] v 1.1", title_align="left", expand=True))

    elif args.singletarget:
        if os.path.exists(sys.argv[1]):
            
            if args.needs_outfile:
                output_file = "customtkinter_" + str(os.path.basename(os.path.splitext(args.targets[0])[0])) + ".py"
            else:
                output_file = args.outfile_value

            make_custom_tkinter(args.targets[0], output_file, args.listbox_flag)

        else:
            console.print(f"cant locate file {sys.argv[1]}")
    
    elif args.multitarget:

        for arg in args.targets:

            if args.has_outfile:
                console.print("[red]User Error[/red]: [italic]Cant use outfile on multiple targets. Reverting to name generator.[/italic]")
            if os.path.exists(arg):
                output_file = "customtkinter_" + str(os.path.basename(os.path.splitext(arg)[0])) + ".py"
                make_custom_tkinter(arg, output_file, args.listbox_flag)
            else:
                console.print(f"cant locate file {arg}")
