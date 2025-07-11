import argparse
from analyzer.CLI_prompting import open_editor, analyze_code

def main():
    parser = argparse.ArgumentParser(
        prog="Complexity Analyzer",
        description="Analyzes code and displays estimated time and space complexity"
    )
    parser.add_argument('--input', type=argparse.FileType('r', encoding="UTF-8"),
                        help='Path to a Python source file to analyze')

    args = parser.parse_args()

    if args.input:
        code = args.input.read()
    else:
        code = open_editor()
        if code is None:
            return  # Canceled

    analyze_code(code)


if __name__ == "__main__":
    main()
