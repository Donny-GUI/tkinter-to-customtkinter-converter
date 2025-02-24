import ast 


class CallNameChanger(ast.NodeTransformer):
    def __init__(self, changes:dict={}):
        self.changes = changes
        if not isinstance(self.changes, dict):
            raise TypeError("changes must be a dictionary")

    def add_change(self, original: str, replacement: str) -> None:
        self.changes[original] = replacement
    

    def visit_Call(self, node: ast.Call) -> ast.Call:
        if isinstance(node.func, ast.Name):
            if node.func.id in self.changes:
                node.func.id = self.changes[node.func.id]
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.attr, ast.Name):
                if node.func.attr.id in self.changes:
                    node.func.attr.id = self.changes[node.func.attr.id]
            elif isinstance(node.func.attr, str):
                if node.func.attr in self.changes:
                    node.func.attr = self.changes[node.func.attr]
        elif ast.unparse(node.func) in self.changes:
            x = self.changes[self.changes[ast.unparse(node.func)]]
            node.func = ast.Name(id=x, ctx=ast.Load())

        return node


class CallArgumentNameChanger(ast.NodeTransformer):
    def __init__(self, changes:dict={}):
        self.changes = changes
        if not isinstance(self.changes, dict):
            raise TypeError("changes must be a dictionary")

    def add_change(self, call_name:str, argument_name: str, replacement: str) -> None:
        """
        Add a new change to the dictionary of changes.

        :param call_name: The name of the function call to modify.
        :param argument_name: The name of the argument to modify in the function call.
        :param replacement: The new name for the argument.
        """

        # Check if the call name already exists in the changes dictionary
        if self.changes.get(call_name, None) is None:
            # If not, create a new dictionary with the argument name and replacement
            self.changes[call_name] = {argument_name: replacement}
        else:
            # If the call name already exists, add the new argument name and replacement to the dictionary
            self.changes[call_name][argument_name] = replacement

    def visit_Call(self, node: ast.Call) -> ast.Call:
        """
        Modify the keyword arguments of a function call based on the changes dictionary.

        :param node: The AST node representing the function call.
        :return: The modified AST node.
        """
        self.generic_visit(node)
        string = ast.unparse(node.func)
        print(string)
        
        # Check if the function name is in the changes dictionary
        if string in self.changes:
            # Iterate over each keyword argument in the function call
            for keyword in node.keywords:
                # Check if the keyword argument name needs to be changed
                kw = ast.unparse(keyword.arg)
                if kw in self.changes[string]:
                    setattr(keyword, 'arg', self.changes[string][kw])
                    keyword.arg = self.changes[string][kw]

        
        # Return the modified node
        return node


class CallArgumentRemover(ast.NodeTransformer):
    def __init__(self, changes:dict={}):
        self.changes = changes
        if not isinstance(self.changes, dict):
            raise TypeError("changes must be a dictionary")

    def add_change(self, call_name:str, argument_name: str) -> None:
        """
        Add a new change to the dictionary of changes.

        :param call_name: The name of the function call to modify.
        :param argument_name: The name of the argument to remove in the function call.
        """

        # Check if the call name already exists in the changes dictionary
        if self.changes.get(call_name, None) is None:
            # If not, create a new dictionary with the argument name and replacement
            self.changes[call_name] = [argument_name]
        else:
            # If the call name already exists, add the new argument name and replacement to the dictionary
            self.changes[call_name].append(argument_name)
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        """
        Modify the keyword arguments of a function call based on the changes dictionary.

        :param node: The AST node representing the function call.
        :return: The modified AST node.
        """
        self.generic_visit(node)
        
        string = ast.unparse(node.func)
        
        # Check if the function name is in the changes dictionary
        if string in self.changes.keys():
            my_keywords = []
            removing_args = self.changes[string]

            # Iterate over each keyword argument in the function call
            for keyword in node.keywords:
                # Check if the keyword argument name needs to be changed
                for arg in removing_args:
                    if keyword.arg == arg:
                        break
                else:
                    my_keywords.append(keyword)

            node.keywords = my_keywords
            setattr(node, 'keywords', my_keywords)
        
        # Return the modified node
        return node
