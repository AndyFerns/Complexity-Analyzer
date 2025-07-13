import streamlit as st
from analyzer.analyzer import ComplexityAnalyzer
from analyzer.parser import parse_code
from analyzer.graph_visualizer import draw_call_graph, plot_Tn_vs_n
import matplotlib.pyplot as plt

st.set_page_config(page_title="Code Complexity Analyzer", layout="wide")
st.title("Code Complexity Analyzer")

code = st.text_area("Paste your Python code here:", height=300, placeholder="def foo(n): ...")

if st.button("Analyze Code"):
    if not code.strip():
        st.warning("Please paste some Python code.")
    else:
        try:
            tree = parse_code(code)
            analyzer = ComplexityAnalyzer()
            time, space = analyzer.analyze(tree)

            st.subheader("Complexity Report")
            st.markdown(f"- **Estimated Time Complexity**: `{time}`")
            st.markdown(f"- **Estimated Space Complexity**: `{space}`")

            # 📄 Line-by-line Annotations
            st.subheader("📄 Annotated Code")
            annotated_lines = code.splitlines()
            for i, line in enumerate(annotated_lines, start=1):
                annotation = analyzer.line_complexities.get(i, "")
                st.code(f"{i:>3} │ {line} {'  # ' + annotation if annotation else ''}", language="python")

            # 📈 T(n) vs n Graph
            if analyzer.function_complexities:
                st.subheader("Time Complexity Plot")
                entry_func = list(analyzer.function_complexities.keys())[0]
                entry_complexity = analyzer.function_complexities[entry_func]

                fig = plot_Tn_vs_n(entry_complexity)
                st.pyplot(fig)

            # 🔗 Call Graph
            st.subheader("Function Call Graph")
            fig2 = plt.figure()
            draw_call_graph(analyzer.call_graph, analyzer.function_complexities)
            st.pyplot(fig2)

        except Exception as e:
            st.error(f"Error: {e}")
