import re
import ast
from copy import deepcopy


tkinter_widgets = [ "Button", "Canvas", "Checkbutton", 
                   "Entry", "Label", "Menubutton", 
                   "Message", "Radiobutton", "Scale", 
                   "Scrollbar", "Text", "Toplevel", 
                   "Treeview", "Frame", "Progressbar", 
                   "Separator"]
ctk_widgets = ["CTk" + x for x in tkinter_widgets]



def change_textvariable_to_variable(source_code: str) -> str:
    """Change occurrences of the parameter 'textvariable' to 'variable' in function calls and class instantiations.

    Args:
        source_code (str): The source code to modify.

    Returns:
        str: The modified source code with 'textvariable' replaced by 'variable'.
    """

    class TextVariableVisitor(ast.NodeTransformer):
        """AST visitor to modify occurrences of 'textvariable' to 'variable'."""

        def visit_Call(self, node: ast.Call) -> ast.Call:
            """Visit function calls and replace 'textvariable' keyword argument with 'variable'."""
            if isinstance(node.func, ast.Name):
                if node.keywords:
                    for keyword in node.keywords:
                        if (
                            isinstance(keyword, ast.keyword)
                            and keyword.arg == "textvariable"
                        ):
                            keyword.arg = "variable"
            return node

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
            """Visit class definitions and replace 'textvariable' keyword argument with 'variable'."""
            for child in node.body:
                if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                    call = child.value
                    if isinstance(call.func, ast.Name):
                        if call.keywords:
                            for keyword in call.keywords:
                                if (
                                    isinstance(keyword, ast.keyword)
                                    and keyword.arg == "textvariable"
                                ):
                                    keyword.arg = "variable"
            return node

    # Parse the source code into an AST
    tree = parsetree(source_code)

    # Transform the AST with the TextVariableVisitor
    transformer = TextVariableVisitor()
    transformed_tree = transformer.visit(tree)

    # Convert the AST back to source code
    modified_source_code = ast.unparse(transformed_tree)

    return modified_source_code

def change_orient_to_orientation(source_code: str) -> str:
    """
    Change occurrences of the parameter 'orient' to 'orientation' 
    in function calls and class instantiations.
    Args:
        source_code (str): The source code to modify.
    Returns:
        str: The modified source code with 'orient' replaced by 'orientation'.
    """

    class OrientVisitor(ast.NodeTransformer):
        """AST visitor to modify occurrences of 'orient' to 'orientation'."""

        def visit_Call(self, node: ast.Call) -> ast.Call:
            """Visit function calls and replace 'orient' keyword argument with 'orientation'."""
            if isinstance(node.func, ast.Name):
                if node.keywords:
                    for keyword in node.keywords:
                        if isinstance(keyword, ast.keyword) and keyword.arg == "orient":
                            keyword.arg = "orientation"
            return node

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
            """Visit class definitions and replace 'orient' keyword argument with 'orientation'."""
            for child in node.body:
                if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                    call = child.value
                    if isinstance(call.func, ast.Name):
                        if call.keywords:
                            for keyword in call.keywords:
                                if (
                                    isinstance(keyword, ast.keyword)
                                    and keyword.arg == "orient"
                                ):
                                    keyword.arg = "orientation"
            return node

    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Transform the AST with the OrientVisitor
    transformer = OrientVisitor()
    transformed_tree = transformer.visit(tree)

    # Convert the AST back to source code
    modified_source_code = ast.unparse(transformed_tree)

    return modified_source_code

def remove_resolution_from_ctkslider(content: str) -> str:
    """
    Remove the 'resolution' parameter from calls to ctk.CTkSlider or CTkSlider
    in the provided Python code.

    Args:
        content (str): The Python code content.

    Returns:
        str: The modified Python code without the 'resolution' parameter.
    """
    tree = parsetree(content)
    slidernodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == "ctk.CTkSlider" or string_name == "CTkSlider":
                n = deepcopy(node)
                slidernodes.append(node)
    for node in slidernodes:
        remove_parameter_from_call(node, "resolution")
    return ast.unparse(tree)

def remove_parameter_from_call(node: ast.Call, parameter: str) -> None:
    """
    Remove the specified parameter from the given AST call node.

    Args:
        node (ast.Call): The AST call node.
        parameter (str): The name of the parameter to remove.

    Returns:
        None
    """
    node.keywords = [kw for kw in node.keywords if kw.arg != parameter]

def parsetree(source: str) -> ast.AST:
    try:
        tree = ast.parse(source, type_comments=True)
    except:
        tree = ast.parse(source)
    finally:
        return tree



class WidgetReplacer:
    """
    A class to replace widgets in a script and add custom constants.

    Attributes:
        source (str): The path to the source script file.
        output (str): The path to the output script file.
        findables (dict): A dictionary containing findable patterns and their replacements.
        constants (list): A list of existing tkinter constants found in the script.
        used_constants (list): A list of constants used in the script.
    """

    tkinter_constants = [
        "ACTIVE",
        "ALL",
        "ANCHOR",
        "ARC",
        "BASELINE",
        "BEVEL",
        "BOTH",
        "BOTTOM",
        "BROWSE",
        "BUTT",
        "CASCADE",
        "CENTER",
        "CHAR",
        "CHECKBUTTON",
        "CHORD",
        "COMMAND",
        "DISABLED",
        "E",
        "END",
        "EW",
        "EXCEPTION",
        "EXTENDED",
        "FALSE",
        "FIRST",
        "FLAT",
        "GROOVE",
        "HIDDEN",
        "HORIZONTAL",
        "INSERT",
        "INSIDE",
        "LAST",
        "LEFT",
        "MITER",
        "MULTIPLE",
        "N",
        "NE",
        "NO",
        "NONE",
        "NORMAL",
        "NS",
        "NSEW",
        "NW",
        "OFF",
        "ON",
        "OUTSIDE",
        "PAGES",
        "PIESLICE",
        "PROJECTING",
        "RADIOBUTTON",
        "RAISED",
        "READABLE",
        "RIDGE",
        "RIGHT",
        "ROUND",
        "S",
        "SCROLL",
        "SE",
        "SEL",
        "SEL_FIRST",
        "SEL_LAST",
        "SEPARATOR",
        "SINGLE",
        "SOLID",
        "SUNKEN",
        "SW",
        "Synchronous",
        "SystemButton",
        "TOP",
        "TRUE",
        "UNITS",
        "VERTICAL",
        "W",
        "WORD",
        "WRITABLE",
        "X",
        "Y",
    ]

    def __init__(self, source: str, output: str) -> None:
        """
        Initialize the WidgetReplacer instance.

        Args:
            source (str): The path to the source script file.
            output (str): The path to the output script file.
        """
        self.source: str = source
        self.output: str = output
        self.findables: dict[str, str] = {}
        self.constants: list[str] = []
        self.used_constants: list[str] = []
    
    def set_source(self, source: str):
        self.source = source
    
    def set_output(self, output: str):
        self.output = output

    def add_findable(self, original: str, replacement: str) -> None:
        """
        Add a findable pattern and its replacement.

        Args:
            original (str): The original pattern to find.
            replacement (str): The replacement pattern.
        """
        self.findables[re.escape(original)] = replacement

    def replace_widgets(self):
        """
        Replace widgets in the script using findable patterns and replacements.
        """
        with open(self.source, "r", encoding="utf-8", errors="ignore") as f:
            script_content = f.read()
        out = ""
        for onst in self.tkinter_constants:
            if re.search(onst, script_content):
                self.constants.append(onst)

        for original, replacement in self.findables.items():
            pattern = r"\b{}\b".format(original)
            script_content = re.sub(pattern, replacement, script_content)

        with open(self.output, "w", errors="ignore") as f:
            f.write(script_content)

    def double_check(self):
        """
        Double-check and add custom tkinter constants to the script.
        """
        with open(self.output, "r") as f:
            script_content = f.readlines()

        out = "import customtkinter as ctk\nfrom customtkinter import "
        m = len(self.constants) - 1
        for index, constant in enumerate(self.constants):
            if index == m:
                out += f"{constant}"
            else:
                out += f"{constant}, "
        out += "\n"

        with open(self.output, "w") as f:
            f.write(out)
            for line in script_content:
                f.write(line)

    def add_constant(self, constant):
        """
        Add a custom constant to the list of constants.

        Args:
            constant (str): The constant to add.
        """
        self.constants.append(constant)



class SourceConverter:

    def __init__(self) -> None:

        self.replacer = WidgetReplacer("None", "None")
        for widget in tkinter_widgets:
            ctk_widget = f"ctk.CTk{widget}"
            self.replacer.add_findable(f" {widget}(", f" {ctk_widget}(")
            self.replacer.add_findable(f"  {widget}(", f"  {ctk_widget}(")
            self.replacer.add_findable(f"{widget}(", f"{ctk_widget}(")
            self.replacer.add_findable(f"{widget}, ", "")
            self.replacer.add_findable(f"{widget},", f"{ctk_widget},")
            self.replacer.add_findable(f" = {widget}(", f" = {ctk_widget}(")
            self.replacer.add_findable(f"={widget}(", f"={ctk_widget}(")
            self.replacer.add_findable(f": {widget} ", f": {ctk_widget} ")
            self.replacer.add_findable(f":{widget},", f":{ctk_widget},")
            self.replacer.add_findable(f":{widget}", f":{ctk_widget}")
        for widg in tkinter_widgets:
            widget = "tk." + widg
            ctk_widget = f"ctk.CTk{widg}"
            self.replacer.add_findable(f"{widget}(", f"{ctk_widget}(")
            self.replacer.add_findable(f" {widget}(", f" {ctk_widget}(")
            self.replacer.add_findable(f"  {widget}(", f"  {ctk_widget}(")
            self.replacer.add_findable(f"{widget}, ", f"")
            self.replacer.add_findable(f"{widget},", f"{ctk_widget},")
            self.replacer.add_findable(f" = {widget}(", f" = {ctk_widget}(")
            self.replacer.add_findable(f"={widget}(", f"={ctk_widget}(")
            self.replacer.add_findable(f": {widget} ", f": {ctk_widget} ")
            self.replacer.add_findable(f":{widget},", f":{ctk_widget},")
            self.replacer.add_findable(f":{widget}", f":{ctk_widget}")
        for widg in tkinter_widgets:
            widget: str = "ttk." + widg
            ctk_widget: str = f"ctk.CTk{widg}"
            self.replacer.add_findable("{0}(".format(widget), "{0}(".format(ctk_widget))
            self.replacer.add_findable("{0}, ".format(widget), "")
            self.replacer.add_findable(widget + ",", "{0},".format(ctk_widget))
            self.replacer.add_findable(" = {0}(".format(widget), " = {0}(".format(ctk_widget))
            self.replacer.add_findable("={0}(".format(widget), "={0}(".format(ctk_widget))
            self.replacer.add_findable(": {0} ".format(widget), ": {0} ".format(ctk_widget))
            self.replacer.add_findable(":{0},".format(widget), ":{0},".format(ctk_widget))
            self.replacer.add_findable(":{0}".format(widget), ":{0}".format(ctk_widget))

    def from_string(self, string: str) -> str:
        script_content = string
        
        self.replacer.constants = []
        for onst in self.replacer.tkinter_constants:
            if re.search(onst, script_content):
                self.replacer.constants.append(onst)

        for original, replacement in self.replacer.findables.items():
            pattern = r"\b{}\b".format(original)
            script_content = re.sub(pattern, replacement, script_content)
        
        out = "import customtkinter as ctk\nfrom customtkinter import "
        m = len(self.replacer.constants) - 1
        for index, constant in enumerate(self.replacer.constants):
            if index == m:
                out += f"{constant}"
            else:
                out += f"{constant}, "
        out += "\n\n"

        script_content = out + script_content
        cont1: str = re.sub(r"\.config\(", ".configure(", script_content)
        cont2 = cont1.replace(", bg=", ", bg_color=").replace(", bg =", ", bg_color =")
        cont3 = cont2.replace(", fg=", ", fg_color=").replace(", fg =", ", fg_color =")
        cont4 = cont3.replace(r"(tk.Tk):", r"(ctk.CTk):")
        for index, widget in enumerate(tkinter_widgets):
            cont4 = cont4.replace(f"(tk.{widget}):", f"(ctk.{ctk_widgets[index]}):")
        cont4 = cont4.replace("(Tk):", "(ctk.CTk):")
        cont5 = cont4.replace("Tk()", "ctk.CTk()")

        lines = cont5.splitlines()
        new_lines = []
        for line in lines:
            l = re.sub(r"ttk.ctk.", r"ctk.", line)
            l2 = re.sub(r"tk.ctk.", r"ctk.", l)
            l3 = re.sub(r".CTkText", r".CTkTextbox", l2)
            l4 = re.sub(r".CTkRadiobutton", r".CTkRadioButton", l3)
            # CTkCheckButton
            l5 = re.sub(r".CTkCheckbutton", r".CTkCheckBox", l4)
            l6 = re.sub(r".CTkScale", r".CTkSlider", l5)
            l7 = l6
            new_lines.append(l7)
        
        source = "\n".join(new_lines)
        try:
            source = change_textvariable_to_variable(source)
        except:
            source = source
        try:
            source = change_orient_to_orientation(source)
        except:
            source = source
        try:
            source = remove_resolution_from_ctkslider(source)
        except:
            source = source
        return source
    
    def from_file(self, filepath: str) -> str:
        with open(filepath, 'r') as f:
            content = f.read()
        return self.from_string(content)
        
        
