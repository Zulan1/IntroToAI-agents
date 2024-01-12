from agent import Agent
from grid import Grid
from type_aliases import Edge
from utils import SearchMinPath

class GreedyAgent(Agent):
    """class for Greedy Agent
    """

    def __init__(self, params: list[str]):
        super().__init__(params)
        self._packages : dict = {}
        self._seq = []
       
    #def ProcessStep(self, grid: Grid, action: Edge):
    #    super().ProcessStep(grid, action)

    def PickPackage(self, grid : Grid) -> None:
        """_summary_

        Args:
            package (Package): Agents picks up package
        """
        package = grid.PickPackage(self._coordinates)
        if package is not None:
            self._packages[package.GetDropoffLoc()] = package
            
    def DropPackage(self) -> None:
        """_summary_

        Args:
            package (Package): Agents picks up package
        """
        if self._coordinates in self._packages:
            del self._packages[self._coordinates]

    def AgentStep(self, grid: Grid, time: int) -> (int, int):
        """Calculates the next step of the Human Agent

        Returns:
            (int, int): The Coordinates the Human agent goes to in the next step.
        """
        self.PickPackage(grid)
        self.DropPackage()
        if self._packages == {}:            
            if self._seq == []:
                nodes = grid.FilterAppearedPackages(time) # goal
                nodesAndFutureNodes = grid.packages()
                if nodesAndFutureNodes == {}:
                    self.done = True
                    return (self.coordinates, self.coordinates)
                self._seq = SearchMinPath(self, grid, nodes) # problem + search
        else:
            if self._seq == []:
                nodes = list(self._packages.keys()) # goal
                self._seq = SearchMinPath(self, grid, nodes) # problem + search
        action: Edge = (self.coordinates, self._seq[0])
        self._seq = self._seq[1:]
        return action
