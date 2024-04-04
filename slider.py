import ast


def remove_resolution_parameter_for_ctk_slider(filepath: str):
    with open(filepath, "r") as r:
        content = r.read()
    modified_code = remove_resolution_from_ctkslider()
    with open(filepath, "w") as w:
        w.write(content)

def remove_parameter_from_call(node: ast.Call, parameter: str):
    node.keywords = [kw for kw in node.keywords if kw.arg != parameter]

def remove_parameter_from_initializer(tree: ast.AST, name: str, parameter: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name == name:
                remove_parameter_from_call(node, parameter)
    return tree

def remove_parameter_from_initializers(tree: ast.AST, names: list[str], parameter: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            if string_name in names:
                remove_parameter_from_call(node, parameter)
    return tree
    
def remove_resolution_from_ctkslider(content: str) -> str:
    tree = ast.parse(content)
    slidernodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            string_name = ast.unparse(node.func)
            print(string_name)
            if string_name == "ctk.CTkSlider" or string_name == "CTkSlider":
                slidernodes.append(node)
    for node in slidernodes:
        remove_parameter_from_call(node, "resolution")
    return ast.unparse(tree)


