from agent import Agent
from grid import Grid
from type_aliases import Node, Edge
from package import Package

class GreedyAgent(Agent):
    """class for Greedy Agent
    """

    def __init__(self, params: list[str]):
        super().__init__(params)
        self._packages : dict[Node, Package] = {}
        self._seq = []
       
    @property
    def packages(self) -> list[Package]:
        """Returns self.packages"""
        return self._packages

    def PickPackage(self, grid: Grid, time: int) -> None:
        """add package to agent when he is on the package's pickup location.

        Args:
            grid(Grid): The simulator's grid.
        """
        package = grid.PickPackage(self._coordinates, time)
        if package is not None:
            self._packages[package.dropoffLoc] = package
            
    def DropPackage(self) -> None:
        """removes package from agent when he is on the package's dropoff location."""
        if self._coordinates in self._packages.keys():
            del self._packages[self._coordinates]

    def AgentStep(self, grid: Grid, time: int) -> Edge:
        """Calculates the next step of the Greedy Agent

        Returns:
            Node: The edge the Greedy Agent traverses in the next step.
        """
        from utils import SearchMinPath

        if self._packages == {}:            
            if self._seq == []:
                nodes = grid.FilterAppearedPackages(time) # goal
                nodesAndFutureNodes = grid.packages.keys()
                if nodesAndFutureNodes == {}:
                    self.done = True
                    return (self.coordinates, self.coordinates)
                self._seq = SearchMinPath(self, grid, nodes) # problem + search
        elif self._seq == []:
            nodes = list(self._packages.keys()) # goal
            self._seq = SearchMinPath(self, grid, nodes) # problem + search
        action: Edge = (self.coordinates, self._seq[0])
        self._seq = self._seq[1:]
        return action
    
    def ProcessStep(self, grid: Grid, action: Edge = None, time: int = 0):
        super().ProcessStep(grid, action)
        self.PickPackage(grid, time)
        self.DropPackage()
