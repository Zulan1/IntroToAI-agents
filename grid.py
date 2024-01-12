from enum import Enum
from typing import Tuple
import networkx as nx
from package import Package
from type_aliases import Node, Edge

class Grid:
    """Simulator's Grid
    """

    def __init__(self, x: int , y: int):
        """Initiallizes connected grid with size x*y

        Args:
            x (int): 1st dimension size
            y (int): 2nd dimension size
        """
        self._size = (x + 1, y + 1)
        # self.nodes = {(i, j) for i in range(x) for j in range(y)}
        # self.edges = {((i, j), (i, j + 1)) for i in range(x) for j in range(y - 1)}
        # self.edges += {((i, j), (i + 1, j)) for i in range(x - 1) for j in range(y)}
        nodes: set[Node] = {(i, j) for i in range(x + 1) for j in range(y + 1)}
        edges = {((i, j), (i, j + 1)) for i in range(x + 1) for j in range(y)}
        edges = edges.union({((i, j), (i + 1, j)) for i in range(x) for j in range(y + 1)})
        self._graph: nx.Graph = nx.Graph()
        self._graph.add_nodes_from(nodes)
        self._graph.add_edges_from(edges)
        self._fragEdges: set[Edge] = set()
        self.packages: list = []
        # self.nodesColors = ["gray" for _ in range(len(self.nodes))]
        # self.edgesColors = ["green" for _ in range(len(self.edges))]
        # self.graph = nx.Graph()

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
            set((int, int), (int, int)): the fragEdges in the grid
        """
        return self._fragEdges

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
        # if self.size[0] != 0 and self.size[1] != 0:
        #     self.nodes = [(i,j) for i in range(self.size[0]) for j in range(self.size[1])]
        #     self.edges = [((i, j), (i, j + 1)) for i in range(self.size[0]) for j in range(self.size[1])]
        #     self.edges += [((i, j), (i + 1, j)) for i in range(self.size[0]) for j in range(self.size[1])]
        #     self.nodes_colors = ["gray" for _ in range(len(self.nodes))]
        #     self.edges_colors = ["green" for _ in range(len(self.edges))]

    def AddPackage(self, params: list[str]):
        """Adds a package to the grid

        Args:
            params (str): parameters of the package
        """
        package = Package(params)
        self.packages.append(package)

class UpdateGridType(Enum):
    """Enum for options to update grid.
    """
    ACTION = 'A'
    BLOCK = 'B'
    FRAGILE = 'F'
    PACKAGE = 'P'

    # def color_packages(self):
    #     for p in self.packages:
    #         match p.get_status():
    #             case "not picked up":
    #                 pass
    #             case "picked up":
    #                 pass
    #             case "dropped off":
    #                 pass
    #             case _:
    #                 print("Somthing went wrong")



    # #Get Methods
    # def get_size(self):
    #     return self.size

    # def get_nodes(self):
    #     return self.nodes

    # def get_edges(self):
    #     return self.edges

    # def get_nodes_colors(self):
    #     return self.nodes_colors

    # def get_edges_colors(self):
    #     return self.edges_colors

    # def get_package(self, package):
    #     return self.packages

    # #Set Methods
    # def set_rows(self, rows):
    #     self.size = (rows, self.size[1])
    #     if self.size[1] != 0:
    #         self.update_board()

    # def set_cols(self, cols):
    #     self.size = (self.size[0], cols)
    #     if self.size[0] != 0:
    #         self.update_board()

    # def set_size(self, rows, cols):
    #     self.size = (rows, cols)
    #     self.update_board()

    # def set_node_color(self, node, color):
    #     if 0 <= node < len(self.nodes_colors):
    #         self.nodes_colors[node] = color

    # def set_edge_color(self, edge, color):
    #     if edge in self.edges:
    #         index = self.edges.index(edge)
    #         self.edges_colors[index] = color
    #     else:
    #         print("Edge does not exist")

    # def set_edge_color_code(self, edge, color_code):
    #     if edge in self.edges:
    #         index = self.edges.index(edge)
    #         self.edges_colors[index] = edge_colors[color_code]
    #     else:
    #         print("Edge does not exist")

    # #doesnt work
    # def draw(self):
    #     pos = {node: (node[1], -node[0]) for node in self.nodes}

    #     # Draw nodes
    #     nx.draw_networkx_nodes(self.graph, pos, node_color=self.nodes_colors, node_size=700)

    #     # Draw edges
    #     nx.draw_networkx_edges(self.graph, pos, edgelist=self.edges, edge_color=self.edges_colors)

    #     # Draw labels (optional)
    #     labels = {node: str(node) for node in self.nodes}
    #     nx.draw_networkx_labels(self.graph, pos, labels)

    #     # Display the plot
    #     plt.show()
        