import ast
from typing import List, Tuple
from .util import parsetree


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
    """Change occurrences of the parameter 'orient' to 'orientation' in function calls and class instantiations.

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
