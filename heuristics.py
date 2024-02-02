import networkx as nx
from grid import Grid
from type_aliases import Node
from utils import Dijkstra, MinimumSpanningTree
from agents.search_agent import SearchAgent
from agents.multi_agent import MultiAgent
import itertools

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
    newGrid = nx.Graph()
    newGrid.add_nodes_from(nodes)
    
    newGrid.add_edges_from((node1, node2, {"weight": len(Dijkstra(grid.graph, node1, node2)) - 1})
                          for node1 in nodes
                          for node2 in nodes
                          if node1 != node2)

    mst = MinimumSpanningTree(newGrid)

    # Get the weights of the edges in the minimum spanning tree
    edgeWeights = [mst[u][v].get("weight", 1) for u, v in mst.edges()]

    return sum(edgeWeights)

def MultiAgentHeuristic(grid: Grid, agentsCoordinates: list[Node], nodes: set[Node]) -> int:
    """Calculates the Multi-Agent Heuristic for the given agents"""
    nodes1, nodes2 = set(), set()
    minCut = float('inf')
    for r in range(len(nodes) + 1):
        for cut in itertools.combinations(nodes, r):
            nodes1 = set(cut)
            nodes2 = nodes - nodes1
            minCut = min(minCut, SalesPersonHeursitic(grid, nodes1.union({agentsCoordinates[0]}))
                          + SalesPersonHeursitic(grid, nodes2.union({agentsCoordinates[1]})))
    return minCut

def MultiAgentHeuristic2(grid: Grid, multiAgent: MultiAgent, i: int) -> int:
    """Calculates the Multi-Agent Heuristic for the given agents"""
    return int(Grid.numOfPackages -
            0.5 * (len(multiAgent.agent1.packages) + len(multiAgent.agent2.packages)) -
            0.25 * len([node for node, t in grid.GetDropdowns() if t <= i]))
