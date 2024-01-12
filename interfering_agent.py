from agent import Agent
from grid import Grid
from type_aliases import Edge
from utils import SearchMinPath

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
            self.seq = SearchMinPath(self, grid, nodes)
        action: Edge = (self.coordinates, self.seq[0])
        self.seq = self.seq[1:]
        return action


    




