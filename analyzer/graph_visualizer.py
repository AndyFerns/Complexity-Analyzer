import networkx as nx
import matplotlib.pyplot as plt

def classify_complexity(complexity_str):
    """
    Classify complexity into color category
    """
    if "n^2" in complexity_str or "n*n" in complexity_str:
        return "red"
    elif "n log n" in complexity_str:
        return "orange"
    elif "n" in complexity_str and "log" not in complexity_str:
        return "yellow"
    elif "log n" in complexity_str:
        return "blue"
    elif "1" in complexity_str:
        return "green"
    else:
        return "lightgray"
    
def draw_call_graph(call_graph, complexities):
    G = nx.DiGraph()
    node_colors = []

    # Add nodes and edges
    for func, calls in call_graph.items():
        complexity = complexities.get(func, "O(?)")
        G.add_node(func, label=f"{func}\n{complexity}")
        node_colors.append(classify_complexity(complexity))
        for callee in calls:
            G.add_edge(func, callee)

    pos = nx.spring_layout(G, k=1.5)

    # Draw graph with color-coded nodes
    labels = {node: f"{node}\n{complexities.get(node, 'O(?)')}" for node in G.nodes()}
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000) # type: ignore 
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')

    plt.title("Function Call Graph with Complexities")
    plt.axis('off')
    plt.tight_layout()
    plt.show()