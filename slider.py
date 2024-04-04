import ast
from util import parsetree


def remove_resolution_parameter_for_ctk_slider(filepath: str) -> None:
    """
    Remove the 'resolution' parameter from all calls to ctk.CTkSlider or CTkSlider
    in the Python file specified by 'filepath'.

    Args:
        filepath (str): The path to the Python file.

    Returns:
        None
    """
    with open(filepath, "r") as r:
        content = r.read()
    modified_code = remove_resolution_from_ctkslider(content)
    with open(filepath, "w") as w:
        w.write(modified_code)

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

def remove_parameter_from_initializer(tree: ast.AST, name: str, parameter: str) -> ast.AST:
    """
    Remove the specified parameter from the initializers with the given name
    in the AST tree.

    Args:
        tree (ast.AST): The AST tree.
        name (str): The name of the initializer.
        parameter (str): The name of the parameter to remove.

    Returns:
        ast.AST: The modified AST tree.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == name:
                remove_parameter_from_call(node, parameter)
    return tree

def remove_parameter_from_initializers(tree: ast.AST, names: list[str], parameter: str) -> ast.AST:
    """
    Remove the specified parameter from the initializers with the given names
    in the AST tree.

    Args:
        tree (ast.AST): The AST tree.
        names (list[str]): The names of the initializers.
        parameter (str): The name of the parameter to remove.

    Returns:
        ast.AST: The modified AST tree.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name in names:
                remove_parameter_from_call(node, parameter)
    return tree
    
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
                n = deep_copy(node)
                slidernodes.append(node)
    for node in slidernodes:
        remove_parameter_from_call(node, "resolution")
    return ast.unparse(tree)


