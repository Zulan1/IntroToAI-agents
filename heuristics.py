import networkx as nx
from grid import Grid
from type_aliases import Node
from utils import Dijkstra, MinimumSpanningTree
from search_agent import SearchAgent

def GetPickUpsAndDropDowns(grid: Grid, agent: SearchAgent) -> set[Node]:
    """Gets all the nodes of packages' pickups or dropoffs

    Args:
        grid (Grid): The Simulator's grid
        agent (GreedyAgent): The agent

    Returns:
        set[Node]: All the grid's pickup and dropoff locations
    """
    relevantNodes = set(grid.packages)
    relevantNodes = relevantNodes.union({p.dropoffLoc for s in grid.packages.values() for p in s})
    relevantNodes = relevantNodes.union({p.dropoffLoc for s in agent.packages.values() for p in s})
    return relevantNodes


def SalesPersonHeursitic(grid: Grid, nodes: set[Node]) -> int:
    """Calculates the Sales Person Heuristic for the given agent"""
    # relevantNodes: set[Node] = GetPickUpsAndDropDowns(grid, agent)
    # relevantNodes.add(startPos)
    newGrid = nx.Graph()
    newGrid.add_nodes_from(nodes)
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2: continue
            newGrid.add_edge(node1, node2, weight=len(Dijkstra(grid.graph, node1, node2)) - 1)

    mst = MinimumSpanningTree(newGrid)

    # Get the weights of the edges in the minimum spanning tree
    edgeWeights = [mst[u][v].get("weight", 1) for u, v in mst.edges()]

    return sum(edgeWeights)
