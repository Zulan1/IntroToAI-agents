import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from grid import Grid
from agent import Agent
from interfering_agent import InterferingAgent
from greedy_agent import GreedyAgent
from type_aliases import Edge

class HumanAgent(Agent):
    """class for Human Agent
    """
    
    def __init__(self, params:list[str], grid: Grid):
        super().__init__(params)
        self.init = False
        pos = nx.spring_layout(grid.graph)
        _, ax = plt.subplots(figsize=(16, 9))
        self.pos = pos
        self.ax = ax
        self.done = True
        i_handle = mpatches.Patch(color='none', label='i = 0')
        brown_handle = mpatches.Patch(color='brown', label='brown = Package')
        green_handle = mpatches.Patch(color='green', label='green = Package Dropoff')
        blue_handle = mpatches.Patch(color='blue', label='blue = Greedy')
        orange_handle = mpatches.Patch(color='orange', label='orange = Human')
        red_handle = mpatches.Patch(color='red', label='red = Interfering')
        self.handles = [i_handle, brown_handle, green_handle, blue_handle, orange_handle, red_handle]
        self.legend = plt.legend(handles=self.handles)
        plt.ion()
        plt.show()

    def AgentStep(self, grid: Grid, agents: list[Agent], i: int) -> Edge:
        """Animates the state of the grid

        Returns:
            Edge: The next edge the Human agent traverses in the next step.
        """
        self.ax.clear()
        edgeColors = ['red' if e in grid.fragEdges or e[::-1] in grid.fragEdges else 'gray' for e in grid.graph.edges()]
        nodeColors = []
        for node in grid.graph.nodes():
            color = '#069AF3'
            for agent in agents:
                if type(agent) == HumanAgent and agent.coordinates == node:
                    color = 'orange'
                if type(agent) == InterferingAgent and agent.coordinates == node:
                    color = 'red'
                if type(agent) == GreedyAgent and agent.coordinates == node:
                    color = '#0000FF'
                if hasattr(agent, 'packages') and node in agent.packages.keys():
                    color = 'green'
            if node in grid.packages.keys():
                color = 'brown'
            nodeColors.append(color)
        nx.draw(grid.graph, self.pos, with_labels = True, node_size=300, ax=self.ax, node_color=nodeColors)
        nx.draw_networkx_edges(grid.graph, self.pos, width=2, edge_color=edgeColors, ax=self.ax)
        i_handle = mpatches.Patch(color='none', label=f'i = {i}')
        self.handles[0] = i_handle
        self.legend.remove()
        plt.legend(handles=self.handles)
        plt.draw()
        plt.pause(0.1)
        
        return (self.coordinates, self.coordinates)