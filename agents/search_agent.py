from abc import ABC, abstractmethod
from agents.agent import Agent
# from agents.astar_agent import AStarAgent
# from agents.interfering_agent import InterferingAgent
from grid import Grid
from package import Package
from type_aliases import Node, Edge

class SearchAgent(Agent, ABC):
    """abstract class for search agents"""
    def __init__(self, params: list[str]) -> None:
        super().__init__(params)
        self.seq: list[Node] = []
        self._packages: dict[Node, set[Package]] = {}
        self._score: int = 0

    @property
    def packages(self) -> list[Package]:
        """Returns self.packages"""
        return self._packages

    @property
    def score(self) -> int:
        """Returns self.score"""
        return self._score

    @abstractmethod
    def Search(self, grid: Grid, nodes: set[Node], i: int) -> None:
        """abstract method for search agents"""
        return []

    @abstractmethod
    def FormulateGoal(self, grid: Grid, i: int) -> set[Node]:
        """abstract method for search agents"""
        return set()

    # @abstractmethod
    def AgentStep(self, grid: Grid, i: int) -> Edge: #, interference: InterferingAgent
        """Calculates the next step of the Search Agent

        Returns:
            Node: The edge the Search Agent traverses in the next step.
        """
        super().AgentStep(grid)
        noOp = (self._coordinates, self._coordinates)

        self.ProcessStep(grid, noOp, i)
        if not self.seq:
            nodes = self.FormulateGoal(grid, i)
            if not nodes:
                self.done = True
                return noOp
            # if isinstance(self, AStarAgent):
            #     self.seq = self.Search(grid, nodes, i, interference)
            # else:
            self.seq = self.Search(grid, nodes, i)

        # Checking the validty of the propesed path
        if not self.seq: return noOp

        action: Edge = (self._coordinates, self.seq[0])
        if (action not in grid.graph.edges() and action[::-1] not in grid.graph.edges()):
            self.seq = []
            return self.AgentStep(grid, i)
        self.seq = self.seq[1:]
        return action

    def ProcessStep(self, grid: Grid, action: Edge = None, i: int = 0):
        super().ProcessStep(grid, action)
        self.PickPackagesFromNode(grid, i)
        self.DropPackage(i)

    def PickPackagesFromNode(self, grid: Grid, i: int) -> None:
        """add package to agent when he is on the package's pickup location.

        Args:
            grid(Grid): The simulator's grid.
        """
        packages = grid.PickPackagesFromNode(self._coordinates, i)
        for package in packages:
            self._packages[package.dropoffLoc] = self._packages.get(package.dropoffLoc, set()).union({package})

    def DropPackage(self, i: int) -> None:
        """removes package from agent when he is on the package's dropoff location."""
        if self._coordinates in self._packages:
            for package in self._packages[self._coordinates]:
                if package.dropoffMaxTime < i: continue
                self._score += 1
            del self._packages[self._coordinates]
