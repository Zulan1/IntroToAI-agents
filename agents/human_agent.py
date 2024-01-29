import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
import networkx as nx
from type_aliases import Node, Edge
from agents.agent import Agent
from agents.interfering_agent import InterferingAgent
from agents.search_agent import SearchAgent
from grid import Grid

class HumanAgent(Agent):
    """class for Human Agent"""

    def __init__(self, params:list[str], grid: Grid):
        super().__init__(params)
        self.init = False
        fig, ax = plt.subplots(figsize=(16, 9))
        self.ax = ax
        self.pos = {(x, y): (x, -y) for x, y in grid.graph.nodes()}
        self.done = True
        self.paused = True
        conButtonAx = fig.add_axes([0, 0.175, 0.1, 0.1], aspect='equal', frameon=False)  # x, y, width, height
        exitButtonAx = fig.add_axes([0, 0.05, 0.1, 0.1], aspect='equal', frameon=False)  # x, y, width, height
        conCircle = mpatches.Circle((0.5, 0.5), 0.5, color='red', transform=conButtonAx.transAxes)
        exitCircle = mpatches.Circle((0.5, 0.5), 0.5, color='red', transform=exitButtonAx.transAxes)
        conButtonAx.add_patch(conCircle)
        exitButtonAx.add_patch(exitCircle)
        self.conButton = Button(conButtonAx, 'Continue', color='none', hovercolor='none')
        self.exitButton = Button(exitButtonAx, 'Exit', color='none', hovercolor='none')
        self.conButton.label.set_color('white')
        self.conButton.label.set_fontsize(14)
        self.exitButton.label.set_color('white')
        self.exitButton.label.set_fontsize(14)
        iHandle = mpatches.Patch(color='none', label='i = 0')
        scoreHandle = mpatches.Patch(color='none', label='Score = 0')
        brownHandle = mpatches.Patch(color='brown', label='- Pickup')
        greenHandle = mpatches.Patch(color='green', label='- Active Dropoff')
        purpleHandle = mpatches.Patch(color='purple', label='- Passive Dropoff')
        blueHandle = mpatches.Patch(color='blue', label='- Greedy')
        redHandle = mpatches.Patch(color='red', label='- Interfering')
        orangeHandle = mpatches.Patch(color='orange', label='- Human')
        self.handles = [iHandle, scoreHandle, brownHandle, greenHandle,
                        purpleHandle, blueHandle, redHandle, orangeHandle]
        self.legend = plt.legend(handles=self.handles)
        plt.ion()
        plt.show()

    def DrawMultiColoredNode(self, node: Node, colors: set[str]):
        """Draws a node in all the colors specified in colors

        Args:
            node (Node): The node to draw
            colors (str[set]): a set of colors to draw the node
        """
        numColors = len(colors)
        for i, color in enumerate(colors):
            # Calculate the angles for the wedge
            theta1 = 90 + 360 * i / numColors
            theta2 = 90 + 360 * (i + 1) / numColors

            # Draw the wedge
            wedge = mpatches.Wedge(center=self.pos[node], r=0.1, theta1=theta1, theta2=theta2, color=color)
            self.ax.add_patch(wedge)

    def ConButtonClick(self, _) -> None:
        """Handles button click"""
        self.paused=False

    def ExitButtonClick(self, _) -> None:
        """Handles button click"""
        sys.exit()

    def AgentStep(self, grid: Grid, agents: list[Agent], i: int) -> Edge:
        """Animates the state of the grid

        Returns:
            Edge: The next edge the Human agent traverses in the next step.
        """
        super().AgentStep(grid, agents, i)
        self.paused = True
        self.conButton.on_clicked(self.ConButtonClick)
        self.exitButton.on_clicked(self.ExitButtonClick)

        self.ax.clear()
        edgeColors = ['red' if e in grid.fragEdges or e[::-1] in grid.fragEdges else 'gray' for e in grid.graph.edges()]
        nx.draw_networkx_edges(grid.graph, self.pos, width=2, edge_color=edgeColors, ax=self.ax)
        for node in grid.graph.nodes():
            colors: set[str] = set()
            for package in sum(grid.packages.values(), []):
                if node == package.dropoffLoc:
                    colors.add('purple')
            if node in grid.packages.keys():
                colors.add('brown')
            for agent in agents:
                if isinstance(agent, HumanAgent) and agent.coordinates == node:
                    colors.add('orange')
                if isinstance(agent, InterferingAgent) and agent.coordinates == node:
                    colors.add('red')
                if isinstance(agent, SearchAgent):
                    if node in agent.packages:
                        colors.add('green')
                    if agent.coordinates == node:
                        colors.add('#0000FF')
            if not colors:
                colors.add('#069AF3')
            self.DrawMultiColoredNode(node, colors)

        nx.draw_networkx_labels(grid.graph, self.pos, ax=self.ax)
        iHandle = mpatches.Patch(color='none', label=f'i = {i}')
        score = [agent.score for agent in agents if isinstance(agent, SearchAgent)][0]
        scoreHandle = mpatches.Patch(color='none', label=f'score = {score}')
        self.handles[0] = iHandle
        self.handles[1] = scoreHandle
        self.legend.remove()
        self.ax.legend(handles=self.handles, loc = (-0.16, 0.6), fontsize=16)
        plt.draw()
        plt.pause(0.1)
        while self.paused:
            plt.pause(0.1)
