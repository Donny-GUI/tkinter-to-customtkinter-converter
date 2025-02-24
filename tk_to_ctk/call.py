import ast

class CallTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self._inside_call = False
        self._call_name = None
        self.name_changes = {}
        self.parameter_removals = {}
        self.argument_value_changes = {}
        self._stack = []

    def add_name_change(self, original: str, replacement: str) -> None:
        self.name_changes[original] = replacement

    def add_argument_name_change(self, call_name: str, argument_name: str, replacement: str) -> None:
        if call_name not in self.name_changes:
            self.name_changes[call_name] = {argument_name: replacement}
        else:
            if not isinstance(self.name_changes[call_name], dict):
                # Convert to dict if it's a direct replacement
                self.name_changes[call_name] = {argument_name: replacement}
            else:
                self.name_changes[call_name][argument_name] = replacement

    def add_keyword_removal(self, call_name: str, argument_name: str) -> None:
        if call_name not in self.parameter_removals:
            self.parameter_removals[call_name] = [argument_name]
        else:
            self.parameter_removals[call_name].append(argument_name)

    def add_argument_value_change(self, call_name: str, argument_name: str, replacement) -> None:
        if call_name not in self.argument_value_changes:
            self.argument_value_changes[call_name] = {argument_name: replacement}
        else:
            self.argument_value_changes[call_name][argument_name] = replacement

    def visit_Call(self, node: ast.Call) -> ast.Call:
        call_name = ast.unparse(node.func)
        
        # Push this call onto the stack
        self._stack.append(call_name)
        self._inside_call = True
        self._call_name = call_name
        
        # Continue with normal visit
        node = self.generic_visit(node)
        
        # Pop from stack when done with this call
        self._stack.pop()
        
        # Update state based on stack
        if self._stack:
            self._call_name = self._stack[-1]
        else:
            self._inside_call = False
            self._call_name = None
            
        return node


class CallNameChanger(CallTransformer):
    def visit_Call(self, node: ast.Call) -> ast.Call:
        # First execute parent's visit_Call to maintain proper stack
        node = super().visit_Call(node)
        
        # Then handle function name changes
        call_name = ast.unparse(node.func)
        if call_name in self.name_changes and isinstance(self.name_changes[call_name], str):
            # Only change if it's a direct name replacement (not arg changes)
            if isinstance(node.func, ast.Name):
                node.func.id = self.name_changes[call_name]
            # Handle attribute calls (e.g., obj.method())
            elif isinstance(node.func, ast.Attribute):
                node.func.attr = self.name_changes[call_name]
        
        return node

    
class CallArgumentRemover(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.parameter_removals = {}
    
    def add_keyword_removal(self, call_name:str, argument_name: str) -> None:
        if self.parameter_removals.get(call_name, None) is None:
            self.parameter_removals[call_name] = [argument_name]
        else:
            self.parameter_removals[call_name].append(argument_name)
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        # First, recursively visit child nodes
        node = self.generic_visit(node)
        
        call_name = ast.unparse(node.func)
        if call_name in self.parameter_removals:
            # Filter out keywords that should be removed
            retained_keywords = []
            for kw in node.keywords:
                arg_name = kw.arg if isinstance(kw.arg, str) else ast.unparse(kw.arg)
                if arg_name not in self.parameter_removals[call_name]:
                    retained_keywords.append(kw)
            
            # Update the node's keywords
            node.keywords = retained_keywords
        
        return node
class CallArgumentNameChanger(CallTransformer):
    def visit_Call(self, node: ast.Call) -> ast.Call:
        # First execute parent's visit_Call to maintain proper stack
        node = super().visit_Call(node)
        
        # Then handle argument name changes
        call_name = ast.unparse(node.func)
        if call_name in self.name_changes and isinstance(self.name_changes[call_name], dict):
            modified_keywords = []
            for kw in node.keywords:
                arg_name = kw.arg if isinstance(kw.arg, str) else ast.unparse(kw.arg)
                if arg_name in self.name_changes[call_name]:
                    # Create a new keyword node with the changed name
                    modified_keywords.append(
                        ast.keyword(self.name_changes[call_name][arg_name], kw.value)
                    )
                else:
                    modified_keywords.append(kw)
            node.keywords = modified_keywords
        
        return node


class CallArgumentValueChanger(CallTransformer):
    def visit_Call(self, node: ast.Call) -> ast.Call:
        # First execute parent's visit_Call to maintain proper stack
        node = super().visit_Call(node)
        
        # Then handle argument value changes
        call_name = ast.unparse(node.func)
        if call_name in self.argument_value_changes:
            modified_keywords = []
            for kw in node.keywords:
                arg_name = kw.arg if isinstance(kw.arg, str) else ast.unparse(kw.arg)
                if arg_name in self.argument_value_changes[call_name]:
                    # Create a new AST node for the replacement value
                    replacement_value = self.argument_value_changes[call_name][arg_name]
                    # Handle if the replacement is already an AST node
                    if not isinstance(replacement_value, ast.AST):
                        replacement_value = ast.parse(str(replacement_value)).body[0].value
                    
                    # Create a new keyword with the same name but different value
                    modified_keywords.append(
                        ast.keyword(kw.arg, replacement_value)
                    )
                else:
                    modified_keywords.append(kw)
            node.keywords = modified_keywords
        
        return node
#
#class CallArgumentNameChanger(ast.NodeTransformer):
#    def __init__(self, changes:dict={}):
#        self.changes = changes
#        if not isinstance(self.changes, dict):
#            raise TypeError("changes must be a dictionary")
#
#    def add_change(self, call_name:str, argument_name: str, replacement: str) -> None:
#        """
#        Add a new change to the dictionary of changes.
#
#        :param call_name: The name of the function call to modify.
#        :param argument_name: The name of the argument to modify in the function call.
#        :param replacement: The new name for the argument.
#        """
#
#        # Check if the call name already exists in the changes dictionary
#        if self.changes.get(call_name, None) is None:
#            # If not, create a new dictionary with the argument name and replacement
#            self.changes[call_name] = {argument_name: replacement}
#        else:
#            # If the call name already exists, add the new argument name and replacement to the dictionary
#            self.changes[call_name][argument_name] = replacement
#
#    def visit_Call(self, node: ast.Call) -> ast.Call:
#        """
#        Modify the keyword arguments of a function call based on the changes dictionary.
#
#        :param node: The AST node representing the function call.
#        :return: The modified AST node.
#        """
#        node = self.generic_visit(node)
#        string = ast.unparse(node.func)
#        print(string)
#        
#        # Check if the function name is in the changes dictionary
#        if string in self.changes:
#            # Iterate over each keyword argument in the function call
#            for keyword in node.keywords:
#                # Check if the keyword argument name needs to be changed
#                kw = ast.unparse(keyword.arg)
#                if kw in self.changes[string]:
#                    setattr(keyword, 'arg', self.changes[string][kw])
#                    keyword.arg = self.changes[string][kw]
#
#        
#        # Return the modified node
#        return node
#
#
#class CallArgumentRemover(ast.NodeTransformer):
#    def __init__(self, changes:dict={}):
#        self.changes = changes
#        if not isinstance(self.changes, dict):
#            raise TypeError("changes must be a dictionary")
#        self._inside_call = False
#        self._call_name = None
#
#    def add_change(self, call_name:str, argument_name: str) -> None:
#        """
#        Add a new change to the dictionary of changes.
#
#        :param call_name: The name of the function call to modify.
#        :param argument_name: The name of the argument to remove in the function call.
#        """
#
#        # Check if the call name already exists in the changes dictionary
#        if self.changes.get(call_name, None) is None:
#            # If not, create a new dictionary with the argument name and replacement
#            self.changes[call_name] = [argument_name]
#        else:
#            # If the call name already exists, add the new argument name and replacement to the dictionary
#            self.changes[call_name].append(argument_name)
#    
#    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
#        if self._inside_call:
#            if self.changes.get(self._call_name, None) != None and node.arg in self.changes[self._call_name]:
#                print(f"[Removing argument]: {node.arg}")
#                return
#
#        return node
#
#    def visit_Call(self, node: ast.Call) -> ast.Call:
#        """
#        Modify the keyword arguments of a function call based on the changes dictionary.
#
#        :param node: The AST node representing the function call.
#        :return: The modified AST node.
#        """
#        self._inside_call = True
#        self._call_name = ast.unparse(node.func)
#
#        self.generic_visit(node)
#        
#        function_name = ast.unparse(node.func)
#        # Print for debugging
#        print(f"Function: {function_name}, Keywords: {[kw.arg for kw in node.keywords]}")        
#        # Check if the function name is in the changes dictionary
#        if function_name in self.changes:
#            removing_args = self.changes[function_name]
#            
#            # Create a new list excluding the keywords we want to remove
#            retained_keywords = []
#            for keyword in node.keywords:
#                if keyword.arg not in removing_args:
#                    retained_keywords.append(keyword)
#                else:
#                    print(f"Removing argument: {keyword.arg}")
#            
#            # Replace the keywords with our filtered list
#            node.keywords = retained_keywords
#        
#        self._inside_call = False
#        return node