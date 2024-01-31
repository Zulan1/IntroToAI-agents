from agents.search_agent import SearchAgent
from grid import Grid
from type_aliases import Node
from package import Package

class StupidGreedyAgent(SearchAgent):
    """class for Stupid Greedy Agent"""

    def __init__(self, params: list[str], _: Grid):
        super().__init__(params, _)
        self._packages: dict[Node, set[Package]] = {}
        self.seq = []

    def FormulateGoal(self, grid: Grid, i: int) -> set[Node]:
        """Formulates the goal of the agent

        Args:
            grid (Grid): the simulator's grid
            i (int): the index of the agent

        Returns:
            set[Node]: the goal of the agent
        """
        if self.packages:
            return set(self.packages.keys())
        nodes: set[Node] = set(grid.FilterAppearedPackages(i).keys())
        nodesAndFutureNodes: set[Node] = set(grid.packages.keys())
        if not nodesAndFutureNodes:
            return set()
        earliestPackages = grid.EarliestPacksage()
        return nodes or earliestPackages or set()

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
