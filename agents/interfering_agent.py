from agents.agent import Agent
from agents.search_agent import SearchAgent
from grid import Grid
from type_aliases import Edge, Node

class InterferingAgent(SearchAgent):
    """Class for Interfering Agent"""

    def __init__(self, params: list[str], _: Grid):
        """Builder function for interfereing agent
        """
        super().__init__(params, _)
        self.seq = []

    def FormulateGoal(self, grid: Grid, _: int) -> set[Node]:
        """Formulates the goal of the agent

        Args:
            grid (Grid): the simulator's grid
            i (int): the index of the agent

        Returns:
            set[Node]: the goal of the agent
        """
        nodes = set(node for node, _ in grid.fragEdges).union(set(node for _, node in grid.fragEdges))
        if self.coordinates in nodes:
            nodes = set(node1 if node2 == self.coordinates else node2
                       for node1, node2, in grid.fragEdges
                       if (node1, node2) == (self.coordinates, node2) or (node1, node2) == (node1, self.coordinates))
        return nodes

    def Search(self, grid: Grid, nodes: set[Node], _, __) -> list[Node]:
        """Searches for the shortest path to the goal

        Args:
            grid (Grid): the simulator's grid
            nodes (set[Node]): the goal

        Returns:
            list[Node]: the shortest path to the goal
        """
        from utils import SearchMinPath

        return SearchMinPath(grid, self.coordinates, nodes)[1:]


    def ProcessStep(self, grid: Grid, action: Edge = None, _: int = 0) -> None:
        Agent.ProcessStep(self, grid, action, _)
