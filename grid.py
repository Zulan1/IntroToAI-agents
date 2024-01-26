from enum import Enum
from typing import Tuple
import networkx as nx
from package import Package
from type_aliases import Node, Edge

class Grid:
    """Simulator's Grid"""
    numOfPackages = 0

    def __init__(self, x: int , y: int):
        """Initiallizes connected grid with size x*y

        Args:
            x (int): 1st dimension size
            y (int): 2nd dimension size
        """
        self._size: Tuple[int, int] = (x + 1, y + 1)
        self._graph: nx.grid_2d_graph = nx.grid_2d_graph(x + 1, y + 1)
        self._fragEdges: set[Edge] = set()
        self._packages: dict[Node, set[Package]] = {}

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the size of the grid"""
        return self._size

    @property
    def graph(self) -> nx.Graph:
        """Returns the networkx graph object"""
        return self._graph

    @property
    def fragEdges(self) -> set[Edge]:
        """returns self.fragEdges

        Args:
            set(Edge): the fragEdges in the grid
        """
        return self._fragEdges

    @property
    def packages(self) -> dict[Node, Package]:
        """returns self._packages

        Returns:
            dict: {Node: Package}
        """
        return self._packages

    def UpdateGrid(self, cmd: str, params: list[str] | Edge) -> None:
        """Updates grid

        Args:
            cmd (str): command used to update the grid
            params (list[str]): parameters to the command
        """
        if cmd == UpdateGridType.ACTION.value:
            if params in self._fragEdges:
                self._graph.remove_edge(*params)
                self._fragEdges.remove(params)
            if params[::-1] in self._fragEdges:
                self._graph.remove_edge(*params[::-1])
                self._fragEdges.remove(params[::-1])
        if cmd == UpdateGridType.BLOCK.value:
            edge = ((int(params[0]), int(params[1])), (int(params[2]), int(params[3])))
            if edge in self.graph.edges():
                self.graph.remove_edge(*edge)
        if cmd == UpdateGridType.FRAGILE.value:
            edge = ((int(params[0]), int(params[1])), (int(params[2]), int(params[3])))
            self._fragEdges.add(edge)
        if cmd == UpdateGridType.PACKAGE.value:
            self.AddPackage(params)

    def AddPackage(self, params: list[str]):
        """Adds a package to the grid

        Args:
            params (str): parameters of the package
        """
        package = Package(params)
        coords = package.pickupLoc
        self._packages[coords] = self._packages.get(coords, set()).union({package})

    def PickPackagesFromNode(self, coords: Node, i: int) -> set[Package]:
        """Return a Package at the location if exists and appeard and delete from grid

        Args:
            coords (Node): check if in these coords there is a package

        Returns:
            Package: Package at the location if exists otherwise None
        """
        packages = set()
        for package in self._packages.get(coords, set()).copy():
            if package.pickupTime <= i:
                packages.add(package)
                self._packages[coords].remove(package)
                if not self._packages[coords]:
                    del self._packages[coords]
        return packages

    def FilterAppearedPackages(self, i: int) -> dict[Package]:
        """return all packages that are currently available

        Args:
            i (int): current iteration

        Returns:
            dict[Package]: Currently available packages
        """
        appearedPackeges: dict[Node, Package] = {coords:\
            {package for package in packages if package.pickupTime <= i}\
                for coords, packages in self._packages.items()}
        appearedPackeges = {coords: packages for coords, packages in appearedPackeges.items() if packages != set()}
        return appearedPackeges

    def EarliestPacksage(self) -> set[Node]:
        """Returns the node of the package that arrives the earliest

        Returns:
            Node: The node of the earliest package
        """
        earliest = (None, None)
        for node, packages in self._packages.items():
            for package in packages:
                if earliest == (None, None) or package.pickupTime < earliest[1]:
                    earliest = ({node}, package.pickupTime)
                if package.pickupTime == earliest[1]:
                    earliest[0].add(node)
        return earliest[0]

class UpdateGridType(Enum):
    """Enum for options to update grid."""
    ACTION = 'ACT'
    BLOCK = 'B'
    FRAGILE = 'F'
    PACKAGE = 'P'
