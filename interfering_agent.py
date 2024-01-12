import networkx as nx
from agent import Agent
from grid import Grid
from type_aliases import Node, Edge

class InterferingAgent(Agent):
    """class for Interfering Agent
    """

    def __init__(self, params: list[str]):
        """Builder function for interfereing agent
        """
        super().__init__(params)
        self.seq = list()


    def AgentStep(self, grid: Grid) -> Edge:
        """Calculates the next step of the Interfering Agent

        Returns:
            Edge: The edge the Interfering agent traverses in the next step.
        """
        actions = list(edge for edge in grid.fragEdges if edge[0] == self.coordinates)
        actions += list(edge[::-1] for edge in grid.fragEdges if edge[1] == self.coordinates)
        if actions != []:
            action = actions[0]
            for edge in actions[1:]:
                if edge[1][0] < action[1][0] or (edge[1][0] == action[1][0] and edge[1][1] < action[1][1]):
                    action = edge
            return action
        if self.seq == []:
            nodes = set(edge[0] for edge in grid.fragEdges).union(set(edge[1] for edge in grid.fragEdges))
            print(f"frag: {grid.fragEdges}")
            if nodes == set():
                self.done = True
                return (self.coordinates, self.coordinates)
            self.seq = self.Search(grid, nodes)
        action: Edge = (self.coordinates, self.seq[0])
        self.seq = self.seq[1:]
        return action


    def Search(self, grid: Grid, nodes: list[Node]) -> list[Node]:
        minPath = grid.graph.nodes()
        for node in nodes:
            path = nx.dijkstra_path(grid.graph, self.coordinates, node)
            minPath = self.ComparePaths(minPath, path)
        # print(f"minPath: {list(minPath)}")
        return list(minPath)



    def ComparePaths(self, path0: list[Node], path1: list[Node]) -> list[Node]:
        if len(path0) < len(path1):
            return path0
        if len(path0) > len(path1):
            return path1
        if len(path0) == len(path1):
            dest0x, dest0y = path0[-1]
            dest1x, dest1y = path1[-1]
            if dest0x < dest1x:
                return path0
            if dest0x > dest1x:
                return path1
            if dest0y < dest1y:
                return path0
            if dest0y > dest1y:
                return path1
