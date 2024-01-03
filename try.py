import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from init_game import init_game

def update(frame):
    # Modify the graph during animation frames
       
    #print(graph[0], '\n')
    pos = nx.planar_layout(graph)
    print(pos, '\n')
    pos = {}
    x = 0    
    for i in range(2):
        for j in range(2):
            pos[x] = (i,j)
            x = x + 1
    #pos = { x: (i%2, (j+1)%2) for i,j,x in zip(range(len(graph.nodes())),range(len(graph.nodes())), range(len(graph.nodes())))}
    print(pos, '\n')
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]
    node_colors = ['gray' if i%2==0 else 'red' for i in range(len(graph.nodes()))]
    if frame == 2:
        edge_colors[3] = 'brown'
        graph[0][2]['color'] = 'brown'
        node_colors[0] = 'blue'
    
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, edgecolors='black')
game = init_game('init_file.txt')

graph = nx.Graph()

# Add nodes to the graph
graph.add_nodes_from(game.get_nodes())

# Add edges to the graph
for edge, color in zip(game.get_edges(), game.get_edges_colors()):
    graph.add_edge(edge[0], edge[1], color=color)

# Create a list of unique colors for nodes
node_colors = game.get_nodes_colors()

# Set up the animation
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, frames=4, interval=2000, repeat=False)  # Update the graph for 2 frames with a 2-second interval

# Show the plot
plt.show()
