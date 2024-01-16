from agent import Agent
from grid import Grid
from type_aliases import Node, Edge
from package import Package

class GreedyAgent(Agent):
    """class for Greedy Agent
    """

    def __init__(self, params: list[str]):
        super().__init__(params)
        self._packages: dict[Node, set[Package]] = {}
        self.seq = []

    @property
    def packages(self) -> list[Package]:
        """Returns self.packages"""
        return self._packages

    def PickPackagesFromNode(self, grid: Grid, time: int) -> None:
        """add package to agent when he is on the package's pickup location.

        Args:
            grid(Grid): The simulator's grid.
        """
        packages = grid.PickPackagesFromNode(self._coordinates, time)
        for package in packages:
            self._packages[package.dropoffLoc] = self._packages.get(package.dropoffLoc, set()).union({package})

    def DropPackage(self) -> None:
        """removes package from agent when he is on the package's dropoff location."""
        if self._coordinates in self._packages:
            del self._packages[self._coordinates]

    def AgentStep(self, grid: Grid, time: int) -> Edge:
        """Calculates the next step of the Greedy Agent

        Returns:
            Node: The edge the Greedy Agent traverses in the next step.
        """
        from utils import SearchMinPath
        super().AgentStep(grid)
        noOp = (self._coordinates, self._coordinates)
        if not self._packages:
            if not self.seq:
                nodes = set(grid.FilterAppearedPackages(time).keys()) # goal
                nodesAndFutureNodes = set(grid.packages.keys())
                if not nodesAndFutureNodes:
                    self.done = True
                    return noOp
                if not nodes:
                    earliestPack: set[Node] = grid.EarliestPackage()
                    self.seq = SearchMinPath(self, grid, earliestPack)[1:]
                else:
                    self.seq = SearchMinPath(self, grid, nodes)[1:] # problem + search
        elif not self.seq:
            nodes = set(self._packages.keys()) # goal
            self.seq = SearchMinPath(self, grid, nodes)[1:] # problem + search

        if not self.seq:
            return noOp
        action: Edge = (self._coordinates, self.seq[0])
        if action not in grid.graph.edges() and action[::-1] not in grid.graph.edges():
            self.seq = []
            return self.AgentStep(grid,time)
        self.seq = self.seq[1:]
        return action

    def ProcessStep(self, grid: Grid, action: Edge = None, time: int = 0):
        super().ProcessStep(grid, action)
        self.PickPackagesFromNode(grid, time)
        self.DropPackage()
