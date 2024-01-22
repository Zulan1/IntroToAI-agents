from utils import MinimumSpanningTree, InitGrid
from grid import Grid
from agent import Agent
from greedy_agent import GreedyAgent
from human_agent import HumanAgent
from heuristics import salesPersonHeursitic
import matplotlib.pyplot as plt
import networkx as nx

def plot_weighted_colored_graph(graph):
    pos = {(x, y): (x, -y) for x, y in grid.graph.nodes()}
    weights = nx.get_edge_attributes(graph, 'weight')

    nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=500)
    nx.draw_networkx_edges(graph, pos, width=2)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color='black')

    # Draw edge weights
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, font_color='red')

    plt.title('Weighted and Colored Graph')
    plt.axis('off')
    plt.show()
    plt.pause(10)
    
filePath = 'tests/test1.txt'
grid: Grid
agents: list[Agent]
grid, agents = InitGrid(filePath)
greedy = [greedy for greedy in agents if isinstance(greedy, GreedyAgent)][0]
mst, h = salesPersonHeursitic(grid, greedy, greedy.coordinates)
print(h)
# grid._graph = mst

plot_weighted_colored_graph(mst)
# hAgent = HumanAgent(['3', '3'], grid)
# hAgent.AgentStep(grid, agents, 1)

