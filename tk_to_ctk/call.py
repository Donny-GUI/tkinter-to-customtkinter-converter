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

    def visit_Module(self, node: ast.Module) -> ast.Module:
        boddy = []
        for b in node.body:
            boddy.append(self.visit(b))
        setattr(node, 'body', boddy)
        return node

    def add_name_change(self, original: str, replacement: str) -> None:
        self.name_changes[original] = replacement

    def add_argument_name_change(self, call_name:str, argument_name: str, replacement: str) -> None:
        if self.name_changes.get(call_name, None) is None:
            
            self.name_changes[call_name] = {argument_name: replacement}
        else:
            self.name_changes[call_name][argument_name] = replacement
        print("self.name_changes ->")
        print(f"Adding argument name change: {call_name}, {argument_name}, {replacement}")


    def add_keyword_removal(self, call_name:str, argument_name: str) -> None:
        if self.parameter_removals.get(call_name, None) is None:
            self.parameter_removals[call_name] = [argument_name]
        else:
            self.parameter_removals[call_name].append(argument_name)
        print("self.parameter_removals ->"  )
        print(f"Adding keyword removal: {call_name}, {argument_name}")


    def add_argument_value_change(self, call_name:str, argument_name: str, replacement: str) -> None:
        if self.name_changes.get(call_name, None) is None:
            self.argument_value_changes[call_name] = {argument_name: replacement}
        else:
            self.argument_value_changes[call_name][argument_name] = replacement
        print("self.argument_value_changes ->")
        print(f"Adding argument value change: {call_name}, {argument_name}, {replacement}")

    def visit(self, node):
        
        if isinstance(node, ast.Call):
            this_name = ast.unparse(node.func)
            self._inside_call = True
            self._call_name = this_name
            self._stack.append(this_name)


        func = getattr(self, 'visit_' + node.__class__.__name__, self.generic_visit)
        print(func.__name__)
        node = func(node)

        if isinstance(node, ast.Call):
            # get last occurance of the call name
            rem = -1
            for index, string in enumerate(self._stack):
                if string == this_name:
                    rem = index
            
            # remove it from the stack
            self._stack.pop(rem)

            # set conditional variables accordingly
            if len(self._stack) == 0:
                # we arent in a call and there is no call name
                self._call_name = None
                self._inside_call = False
            else:
                # we are nested in a call and there is a call name, which was the last one we were in. 
                self._call_name = self._stack[-1]
                self._inside_call = True

        return func(node)

class CallNameChanger(CallTransformer):
    def __init__(self):
        super().__init__(self)

    def visit_Call(self, node: ast.Call) -> ast.Call:
        if self._inside_call and self._call_name in self.name_changes:
            node.func.id = self.name_changes[self._call_name]
            setattr(node.func, 'id', self.name_changes[self._call_name])
        return node

class CallArgumentRemover(CallTransformer):
    def __init__(self):
        CallTransformer.__init__(self)
    
    def visit_Module(self, node: ast.Module) -> ast.Module:
        boddy = []
        for b in node.body:
            boddy.append(self.visit(b))
        setattr(node, 'body', boddy)
        return node

    def visit_Call(self, node: ast.Call) -> ast.Call:
        self._call_name = ast.unparse(node.func)
        if self.parameter_removals.get(self._call_name, None):
            mykws = []
            for kw in node.keywords:
                str_kw_arg = ast.unparse(kw.arg)
                if self.parameter_removals.get(self._call_name).get(str_kw_arg, None):
                    continue
                mykws.append(kw)
            node.keywords = mykws
            setattr(node, 'keywords', mykws)
            return node

        return node

class CallArgumentNameChanger(CallTransformer):
    def __init__(self):
        CallTransformer.__init__(self)
    
    def visit_Module(self, node: ast.Module) -> ast.Module:
        boddy = []
        for b in node.body:
            boddy.append(super().visit(b))
        setattr(node, 'body', boddy)
        return node

    def visit_Call(self, node: ast.Call) -> ast.Call:
        self._call_name = ast.unparse(node.func)
        if self._inside_call and self._call_name in self.name_changes:
            mykws = []
            for kw in node.keywords:
                if ast.unparse(kw.arg) in self.name_changes[ast.unparse(node.func)]:
                    mykws.append(ast.keyword(self.name_changes[ast.unparse(node.func)][ast.unparse(kw.arg)], kw.value))
                else:
                    mykws.append(kw)
            node.keywords = mykws
            setattr(node, 'keywords', mykws)

        return node

    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
        self._keyword_name = ast.unparse(node.arg)

        if self._inside_call and self._call_name in self.name_changes:
            na = ast.unparse(node.arg)
            if na in self.name_changes[self._call_name]:
                node.arg = self.name_changes[self._call_name][na]
        return node

class CallArgumentValueChanger(CallTransformer):
    def __init__(self):
        CallTransformer.__init__(self)
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        self._call_name = ast.unparse(node.func)
        if ast.unparse(node.func) in self.argument_value_changes:
            mykws = []
            for kw in node.keywords:
                if ast.unparse(kw.arg) in self.argument_value_changes[ast.unparse(node.func)]:
                    mykws.append(ast.keyword(kw.arg, self.argument_value_changes[ast.unparse(node.func)][ast.unparse(kw.arg)]))
                else:
                    mykws.append(kw)
            node.keywords = mykws
            setattr(node, 'keywords', mykws)

        return node

    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
        na = ast.unparse(node.value)
        if na in self.argument_value_changes[self._call_name]:
            node.value = self.name_changes[self._call_name][ast.unparse(node.arg)]
            setattr(node, 'value', self.name_changes[self._call_name][ast.unparse(node.arg)])
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