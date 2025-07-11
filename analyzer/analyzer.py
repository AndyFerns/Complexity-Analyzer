import ast

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
        self.loop_count = 0
        self.recursive = False

    def visit_For(self, node):
        self.loop_count += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.loop_count += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if any(isinstance(n, ast.Call) and n.func.id == node.name #type:ignore
               for n in ast.walk(node)):
            self.recursive = True
        self.generic_visit(node)

    def analyze(self, tree):
        self.visit(tree)
        time = f"O(n^{self.loop_count})"
        if self.recursive:
            time += " + Recursion"
        return time, "Space analysis TODO"
