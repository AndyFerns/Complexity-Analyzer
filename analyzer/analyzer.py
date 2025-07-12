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

    def analyze(self, tree):
        self.visit(tree)
        time = f"O(n^{self.loop_count})"
        space = f"O({self.var_space + self.data_structures}) vars"
        
        if self.recursive:
            time += " + Recursion"
            space += " + call stack"
        return time, space
