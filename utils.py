import networkx as nx
from grid import Grid, UpdateGridType
from agents.agent import Agent, AgentType
from agents.human_agent import HumanAgent
from agents.interfering_agent import InterferingAgent
from agents.stupid_greedy_agent import StupidGreedyAgent
from agents.greedy_agent import GreedyAgent
from agents.astar_agent import AStarAgent
from agents.rtastar_agent import RTAStarAgent
from agents.multi_agent import MultiAgent
from type_aliases import Node

agent_classes = {
    AgentType.STUPID_GREEDY.value: StupidGreedyAgent,
    AgentType.GREEDY.value: GreedyAgent,
    AgentType.A_STAR.value: AStarAgent,
    AgentType.RTA_STAR.value: RTAStarAgent,
    AgentType.HUMAN.value: HumanAgent,
    AgentType.INTERFERING.value: InterferingAgent,
    AgentType.MULTI_AGNENT.value: MultiAgent
}

def InitGrid(initFilePath: str) -> (Grid, list[Agent]):
    """initializes grid from init file

    Args:
        initFilePath (str): init file path

    Returns:
        Grid: Simulator's grid
        list[Agent]: the agents activated in the simulator
    """
    with open(initFilePath, 'r') as f:
        # find all lines starting with '#' and cut them off on ';'
        lines = list(line.split(';')[0].split('#')[1].strip().split(' ')
                     for line in f.readlines() if line.startswith("#"))  # seperate the line to a list of words/tokens.
        lines = list(list(filter(lambda e: e!='', line)) for line in lines) # filter empty words/tokens

    x = list(int(line[1]) for line in lines if line[0].lower() == 'x')[0] # extract x max value from file
    y = list(int(line[1]) for line in lines if line[0].lower() == 'y')[0] # extract y max value from file

    grid: Grid = Grid(x, y)

    for line in lines:
        action = line[0]
        # if action is of updating the grid type then call UpdateGrid
        if any(action == updateGridType.value for updateGridType in UpdateGridType):
            grid.UpdateGrid(action, line[1:])

    agents: list[Agent] = []
    for line in lines: # build the agents specified in the file
        action = line[0]
        if action not in agent_classes: continue
        agents.append(agent_classes[action](line[1:], grid))

    for agent in agents:
        agent.ProcessStep(grid)

    Grid.numOfPackages = len(sum(grid.packages.values(), []))
    lastDropOffTime = max(p.dropOffMaxTime for p in sum(grid.packages.values(), []))
    Agent.lastDropOffTime = lastDropOffTime

    return grid, agents

def SearchMinPath(grid: Grid, start: Node, nodes: set[Node]) -> list[Node]:
    """searches the shortest path between 1 start node and multiple target nodes

    Args:
        grid (Grid): the simulator's grid
        nodes (list[Node]): a list of target nodes

    Returns:
        list[Node]: the shortest path to the closest target node
    """
    minPath = None
    for node in nodes:
        path = Dijkstra(grid.graph, start, node)
        minPath = ComparePaths(minPath, path)
    return list(minPath)

def ComparePaths(path0: list[Node], path1: list[Node]) -> list[Node]:
    """Compares 2 paths and chooses the shortest path. chooses lower x value, and then y value in case of ties.

    Args:
        path0 (list[Node]): a path between 2 nodes
        path1 (list[Node]): a different path between 2 nodes

    Returns:
        list[Node]: shortest path
    """
    if path0 is None or (path1 is not None and len(path1) < len(path0)):
        return path1
    if path1 is None or (len(path0) < len(path1)):
        return path0
    return min(path0, path1, key=lambda path: (path[-1].x, path[-1].y))

def Dijkstra(g: nx.Graph, start: Node, end: Node) -> list[Node]:
    """dijkstra algorithm implementation

    Args:
        g (nx.Graph): a graph
        start (Node): start node
        end (Node): end node

    Returns:
        list[Node]: the shortest path between start and end
    """
    dist = {start: 0}
    prev = {}
    q = set(g.nodes())
    while q:
        u = min(q, key=lambda node: dist.get(node, float('inf')))
        q.remove(u)
        if u == end:
            break
        for v in g.neighbors(u):
            alt = dist[u] + g[u][v].get('weight', 1)
            if alt < dist.get(v, float('inf')):
                dist[v] = alt
                prev[v] = u
    path = []
    u = end
    while u in prev:
        path.insert(0, u)
        u = prev[u]
    path.insert(0, u)
    return path

def MinimumSpanningTree(g: nx.Graph) -> nx.Graph:
    """Kruksal's minimum spanning tree algorithm implementation

    Args:
        g (nx.Graph): a graph

    Returns:
        nx.Graph: the minimum spanning tree of g
    """
    mst = nx.Graph()
    mst.add_nodes_from(g.nodes)
    edges = sorted(g.edges(data=True), key=lambda edge: edge[2].get('weight', 1))
    
    for edge in edges:
        if not nx.has_path(mst, edge[0], edge[1]):
            mst.add_edge(edge[0], edge[1], weight=edge[2].get('weight', 1))
    return mst
