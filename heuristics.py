import networkx as nx
from grid import Grid
from type_aliases import Node
from utils import Dijkstra, MinimumSpanningTree
from greedy_agent import GreedyAgent

def getPickUpsAndDropDowns(grid: Grid, agent: GreedyAgent) -> set[Node]:
    relevantNodes = set(grid.packages)
    relevantNodes = relevantNodes.union({p.dropoffLoc for s in grid.packages.values() for p in s})
    relevantNodes = relevantNodes.union({p.dropoffLoc for s in agent.packages.values() for p in s})
    return relevantNodes


def salesPersonHeursitic(grid: Grid, agent: GreedyAgent, currentNode: Node) -> int:
    relevantNodes: set[Node] = getPickUpsAndDropDowns(grid, agent)
    relevantNodes.add(currentNode)
    newGrid = nx.Graph()
    newGrid.add_nodes_from(relevantNodes)
    for node1 in relevantNodes:
        for node2 in relevantNodes:
            if node1 != node2:
                newGrid.add_edge(node1, node2, weight=len(Dijkstra(grid.graph, node1, node2)) - 1)

    mst = MinimumSpanningTree(newGrid)
    #return sum(e[2]["weight"] for e in mst.edges())
    return mst, sum(mst[u][v]["weight"] for u,v in mst.edges())
