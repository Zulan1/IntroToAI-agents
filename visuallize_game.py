import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
def create_colored_graph(edges, nodes, edge_colors):
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(nodes)

    # Add edges to the graph
    G.add_edges_from(edges)

    # Specify three distinct colors for edges
    

    # Create a list of unique colors for nodes
    node_colors = ['gray' if i%2==0 else 'red' for i in range(len(edges))]

    # Draw the graph with specified colors
    pos = nx.spring_layout(G)  # You can use other layout algorithms as well
    for i in range(100):
        nx.draw(G, pos, with_labels=False, node_color=node_colors, edge_color=edge_colors)
        node_colors = ['gray' if i%2==0 else 'red' for j in range(len(edges))]
        sleep(1)

    # Show the plot
    plt.show()

# Example usage
edges = [(0, 1), (0, 2), (1, 2), (1, 4), (2, 3)]
nodes = [0, 1, 2, 3]
edge_colors = ['blue', 'blue', 'red', 'red', 'black']#['blue' if i%2==0 else 'green' for i in range(len(edges))]

create_colored_graph(edges, nodes, edge_colors)
