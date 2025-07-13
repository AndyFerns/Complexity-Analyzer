from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from analyzer.parser import parse_code
from analyzer.analyzer import ComplexityAnalyzer
from analyzer.graph_visualizer import draw_call_graph, plot_Tn_vs_n

def open_editor():
    session = PromptSession(multiline=True)

    bindings = KeyBindings()

    @bindings.add("f2")
    def _(event):
        event.app.exit(result=event.app.current_buffer.text)

    @bindings.add("escape")
    def _(event):
        print("\nEditor canceled.")
        event.app.exit(result=None)

    print("\nEnter your Python code below:")
    print("Press F2 to analyze, Esc to cancel.\n")

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
        
        # Inline complexity annotation Suite:
        print("\n📄 Complexity Annotated Code:")
        lines = code.splitlines()
        for i, line in enumerate(lines, start=1):
            complexity = analyzer.line_complexities.get(i, "")
            tag = f"  # {complexity}" if complexity else ""
            print(f"{i:3} │ {line:<50}{tag}")
            
        
        # Draw graph
        draw_call_graph(analyzer.call_graph, analyzer.function_complexities)
        
        # Plot T(n) vs n for top-level function (usually main or first function)
        if analyzer.function_complexities:
            entry_func = list(analyzer.function_complexities.keys())[0]
            entry_complexity = analyzer.function_complexities[entry_func]
            plot_Tn_vs_n(entry_complexity)
            
    except Exception as e:
        print(f"\nError: {e}")