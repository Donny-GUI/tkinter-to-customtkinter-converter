import re
import os
import subprocess
from util import pip_str, get_listbox_source, has_listbox, classes_begin_index, print_warning
from lists import tkinter_widgets, ctk_widgets
from templates import print_examples, print_help_screen
try:
    from rich.status import Status
except:
    print(f"rich is not installed. Installing...")
    subprocess.run([pip_str, "install", "rich"], check=True)
    print(f"rich has been installed.")
from rich.status import Status
from widget_replacer import WidgetReplacer
from app_parser import get_parser


Gverbose = False


##################################################
# FUNCTIONS
##################################################

def verbose_print(string: str) -> None:
    global Gverbose
    if Gverbose:
        print(string)

def replace_bg_with_bg_color_in_file(file_path:str) -> None:
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
        cont = cont.replace(f"(tk.{widget}):",f"(ctk.{ctk_widgets[index]}):")
    cont = cont.replace("(Tk):", "(ctk.CTk):")
    cont = cont.replace("Tk()", "ctk.CTk()")
    verbose_print(f"Writing new content to {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cont)

def replace_config_with_configure(file_path:str) -> None:
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
    modified_content = re.sub(r'\.config\(', '.configure(', content)
    verbose_print(f"Writing {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(modified_content)

def find_errs(file_path:str) -> None:
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
            l = re.sub(r'ttk.ctk.', r'ctk.', line)
            l2 = re.sub(r'tk.ctk.', r'ctk.', l)
            l3 = re.sub(r'.CTkText', r'.CTkTextbox', l2)
            l4 = re.sub(r'.CTkRadiobutton', r'.CTkRadioButton', l3)
            #CTkCheckButton
            l5 = re.sub(r'.CTkCheckbutton', r'.CTkCheckBox', l4)
            l6 = re.sub(r'.CTkScale', r'.CTkSlider', l5)
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
        content1 = re.sub(r"ttk.Listbox(", r"CTkListbox(", content)
        content2 = re.sub(r"tk.Listbox(", r"CTkListbox(", content1)
        # write the final content
        with open(filepath, "w") as w:
            w.write(content2)

def make_custom_tkinter(input_file:str, output_filename: str, convert_listboxes: bool=False, verbose: str=False) -> None:
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
        status.update(" ttk.Widget -> ctk.CTkWidget" )

        verbose_print("Iterating through ttk widgets for regex patterns...")
        for widg in tkinter_widgets:
            widget:str = "ttk." + widg
            ctk_widget:str = f"ctk.CTk{widg}"
            verbose_print(widget)
            wr.add_findable("{0}(".format(widget), "{0}(".format(ctk_widget))
            wr.add_findable("{0}, ".format(widget), "")
            wr.add_findable(widget+",", "{0},".format(ctk_widget))
            wr.add_findable(" = {0}(".format(widget), " = {0}(".format(ctk_widget))
            wr.add_findable("={0}(".format(widget), "={0}(".format(ctk_widget))
            wr.add_findable(": {0} ".format(widget), ": {0} ".format(ctk_widget))
            wr.add_findable(":{0},".format(widget),  ":{0},".format(ctk_widget))
            wr.add_findable(":{0}".format(widget), ":{0}".format(ctk_widget))
        
        verbose_print("Replacing all widgets now...")
        status.update("Replacing all widgets...")
        wr.replace_widgets()
        
        verbose_print("Double checking widgets now...")
        status.update("Double checking constants...")
        wr.double_check()

        status.update("finding .config/.configure...")
        verbose_print("Finding .config/.configure to replace...")
        replace_config_with_configure(file_path =output_filename)
        
        status.update("finding bg/bg_color...")
        verbose_print("finding bg parameter to convert to bg_color...")
        replace_bg_with_bg_color_in_file( file_path =output_filename)
        
        status.update("finding fg/fg_color...")
        verbose_print("finding fg parameter to convert to fg_color")
        replace_fg_with_fg_color_in_file(file_path =output_filename)
        
        status.update("    finding meta class options...")
        verbose_print("finding meta class tkinter objects...")
        replace_meta_in_file(file_path = output_filename)
        
        status.update("Checking for errors...")
        verbose_print("checking for errors...")
        find_errs(file_path = output_filename)
        
        if convert_listboxes:
            status.update(" fixing the listboxes...")
            verbose_print("Converting listboxes as specified by listbox flag...")
            rewrite_listboxes(file_path = output_filename)

        verbose_print(output_filename)
        verbose_print("done.")

def input_filename_to_output_filename(input_filename: str) -> str:
    return os.path.join(os.getcwd(), "customtkinter_" + os.path.basename(str(input_filename)))

def main():
    global Gverbose

    parser = get_parser()
    print(parser.parse_args())

    try:
        args = parser.parse_args()
    except:
        print_warning(" -m/--multiple flag expected at least one argument")
        return
        
    Gverbose = args.Verbose
    verbose_print("Checking Flags...")

    if args.Examples:
        print_examples()

    if args.Target == None and args.Multiple == None:
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

    elif args.Output == None:
        verbose_print("Output not specified, making one from input file")
        args.Output = input_filename_to_output_filename(args.Target)

    if args.Multiple:
        verbose_print("Multiple conversions underway...")

        if args.Output:
            verbose_print("Multiple flag used with outfile flag, defaulting to name generator...")
            print_warning("Cant specify output file with multiple conversions")
        
        for index, item in enumerate(args.Multiple):
            verbose_print(f"Conversion {index+1} : {item}")
            output = input_filename_to_output_filename(item)
            make_custom_tkinter(input_file=item, output_filename=output, convert_listboxes=parser.Listboxes, verbose=args.Verbose)
    
    else:
        verbose_print("Single Target conversion underway...")
        if os.path.exists(str(parser.Target)):
            make_custom_tkinter(input_file=parser.Target, 
                                output_file=parser.Output, 
                                convert_listboxes=parser.Listboxes, 
                                verbose=args.Verbose)
        else:
            trypath = os.path.join(os.getcwd(), os.path.basename(str(parser.Target)))
            if os.path.exists(trypath):
                make_custom_tkinter(input_file=trypath, 
                                    output_file=parser.Output, 
                                    convert_listboxes=parser.Listboxes, 
                                    verbose=args.Verbose)
            else:
                print_warning(f"Could not find file {parser.Target}")
                return


if __name__ == "__main__":
    main()