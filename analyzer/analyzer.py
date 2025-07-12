import ast
import sys

class ComplexityAnalyzer(ast.NodeVisitor):
    '''
    Main Class for analyzing given code complexity

    Functions:\n
    visit_For(self, node)\n
    visit_While(self, node)\n
    visit_FunctionDef(self, node)\n
    visit_Assign(self, node)\n
    analyze(self, tree)\n
    '''
    def __init__(self):
        # Time Complexity suite
        self.loop_count = 0
        self.recursive = False
        self.recursive_calls = 0 # Count of recursive calls inside function
        self.func_name = set()

        # NEW: Track loop nesting and pattern types
        self.nesting_depth = 0
        self.max_nesting = 0
        self.has_log_loop = False  # e.g., while n > 1: n //= 2

        # Space Complexity suite
        self.var_space = 0
        self.data_structures = 0

        # Input variable tracking
        self.input_vars = set()
        
        # Line complexity annotation Suite
        self.line_complexities = {}  # Dict[line_no] = complexity str
        
        self.divide_factor_detected = False # True if n//2 or slicing is found

    def visit_For(self, node):
        self.loop_count += 1

        # NEW: Nesting depth for nested loops
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        
        self.line_complexities[node.lineno] = "O(n)"  # loop = linear

        # NEW: Try to detect range(n) dependency
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == "range":
                args = node.iter.args
                if args:
                    last_arg = args[-1]
                    if isinstance(last_arg, ast.Name) and last_arg.id in self.input_vars:
                        pass  # Loop depends on input — symbolic O(n)

        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_While(self, node):
        self.loop_count += 1
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)\
            
        self.line_complexities[node.lineno] = "O(n)"  # loop = linear

        # NEW: Detect logarithmic patterns like n = n // 2
        assigns = [n for n in ast.walk(node) if isinstance(n, (ast.Assign, ast.AugAssign))]
        for a in assigns:
            if isinstance(a, ast.AugAssign):
                if isinstance(a.op, ast.FloorDiv):
                    self.has_log_loop = True
            elif isinstance(a, ast.Assign):
                if isinstance(a.value, ast.BinOp) and isinstance(a.value.op, ast.FloorDiv):
                    self.has_log_loop = True

        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_Assign(self, node):
        # Estimate space by counting data structures assigned
        if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            self.data_structures += 1
        self.var_space += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_func = node.name

        # NEW: Track function arguments as input variables
        for arg in node.args.args:
            self.input_vars.add(arg.arg)

        # Check for recursion
        if any(
            isinstance(n, ast.Call) and 
            isinstance(n.func, ast.Name) and 
            n.func.id == node.name
            for n in ast.walk(node)
        ):
            self.recursive = True
            self.recursive_calls += 1
            
        # Detect input division like n // 2 or slicing [:len()//2]
        for n in ast.walk(node):
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.FloorDiv):
                self.divide_factor_detected = True
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
                self.divide_factor_detected = True

        self.generic_visit(node)
        
        if self.recursive:
            self.line_complexities[node.lineno] = f"O({self.recursive_calls}T(n/{'2' if self.divide_factor_detected else 'n'}) + ...)"


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

        # Time Complexity Suite 
        time_parts = []

        # e.g., while n > 1: n //= 2
        if self.has_log_loop:
            time_parts.append("log n")

        # Loop nesting depth → multiplicative n's
        for _ in range(self.max_nesting):
            time_parts.append("n")

        # If recursion is used, add hint
        if self.recursive:
            time_parts.append("recursion")

        if time_parts:
            time = "O(" + " ".join(time_parts) + ")"
        else:
            time = "O(1)"

        # Space Complexity est. suite 
        space_bytes = self.var_space * sys.getsizeof(0)  # assume integers
        space_bytes += self.data_structures * sys.getsizeof([])  # assume empty lists

        if self.recursive and self.recursive_calls >= 1 and self.divide_factor_detected:
            # Classic divide-and-conquer
            if self.recursive_calls == 2:
                time = "O(n log n)"
            elif self.recursive_calls == 1:
                time = "O(log n)"
            else:
                time = f"O(n^{self.recursive_calls} log n)"
            space_bytes += 1024 * (self.loop_count + 1)  # assume ~1KB per stack frame
        else:
            if self.has_log_loop:
                time_parts.append("log n")
            for _ in range(self.max_nesting):
                time_parts.append("n")
            if self.recursive:
                time_parts.append("recursion")
            time = "O(" + " ".join(time_parts) + ")" if time_parts else "O(1)"

        space = self._format_memory_size(space_bytes)
        return time, space
