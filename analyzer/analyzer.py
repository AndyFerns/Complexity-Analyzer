import ast
import sys

class ComplexityAnalyzer(ast.NodeVisitor):
    '''
    Main Class for analyzing given code complexity
    
    Functions:\n
    visit_For(self, node)\n
    visit_While(self, node)\n
    visit_FunctionDef(self, node)\n
    analyze(self, tree)\n
    '''
    def __init__(self):
        # Time Complexity suite
        self.loop_count = 0
        self.recursive = False
        
        # Space Complexity suite
        self.var_space = 0
        self.data_structures = 0
        self.func_name = set()

    def visit_For(self, node):
        self.loop_count += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.loop_count += 1
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        # Estimate space by counting data structures assigned
        if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            self.data_structures += 1
        self.var_space += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if any(
            isinstance(n, ast.Call) and 
            isinstance(n.func, ast.Name)
            and n.func.id == node.name 
            for n in ast.walk(node)
        ):
            self.recursive = True
            
        self.generic_visit(node)
        
    def _format_memory_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{size_bytes / (1024 ** 3):.2f} GB"

    def analyze(self, tree):
        self.visit(tree)
        time = f"O(n^{self.loop_count})"
        if self.recursive:
            time += " + recursion"

        # Estimate space: base size of each variable/data structure
        space_bytes = self.var_space * sys.getsizeof(0)  # Assume integers
        space_bytes += self.data_structures * sys.getsizeof([])  # Assume empty lists

        if self.recursive:
            # Assume ~1KB stack frame per recursive call (rough)
            space_bytes += 1024 * (self.loop_count + 1)

        space = self._format_memory_size(space_bytes)
        return time, space
