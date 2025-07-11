import ast

def parse_code(source):
    try:
        return ast.parse(source)
    except Exception as e:
        print(f"[ERROR] {e}")