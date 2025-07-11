from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from analyzer.parser import parse_code
from analyzer.analyzer import ComplexityAnalyzer

def open_editor():
    session = PromptSession(multiline=True)

    bindings = KeyBindings()

    @bindings.add("c-enter")
    def _(event):
        event.app.exit(result=event.app.current_buffer.text)

    @bindings.add("escape")
    def _(event):
        print("\nEditor canceled.")
        event.app.exit(result=None)

    print("\nEnter your Python code below:")
    print("Press Ctrl+Enter to analyze, Esc to cancel.\n")

    code = session.prompt(
        "> ",
        multiline=True,
        key_bindings=bindings,
        style=Style.from_dict({
            "prompt": "#00ff00",
        })
    )
    return code

def analyze_code(code):
    try:
        tree = parse_code(code)
        analyzer = ComplexityAnalyzer()
        time, space = analyzer.analyze(tree)
        print("\n📊 Complexity Report:")
        print(f"  ⏱️ Estimated Time Complexity: {time}")
        print(f"  🧠 Estimated Space Complexity: {space}")
    except Exception as e:
        print(f"\nError: {e}")