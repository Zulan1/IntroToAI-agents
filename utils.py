import networkx as nx
from grid import Grid, UpdateGridType
from agent import Agent, AgentType
from human_agent import HumanAgent
from interfering_agent import InterferingAgent
from greedy_agent import GreedyAgent
from type_aliases import Node

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
        if not any(action == agentType.value for agentType in AgentType): continue
        if action == AgentType.GREEDY.value:
            agents.append(GreedyAgent(line[1:]))
        if action == AgentType.HUMAN.value:
            agents.append(HumanAgent(line[1:], grid))
        if action == AgentType.INTERFERING.value:
            agents.append(InterferingAgent(line[1:]))

    for agent in agents:
        agent.ProcessStep(grid)

    return grid, agents

def SearchMinPath(self, grid: Grid, nodes: list[Node]) -> list[Node]:
    """searches the shortest path between 1 start node and multiple target nodes

    Args:
        grid (Grid): the simulator's grid
        nodes (list[Node]): a list of target nodes

    Returns:
        list[Node]: the shortest path to the closest target node
    """
    minPath = None
    for node in nodes:
        path = nx.dijkstra_path(grid.graph, self.coordinates, node)
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
    if path0 is None:
        return path1
    if path1 is None:
        return path0
    if len(path0) < len(path1):
        return path0
    if len(path0) > len(path1):
        return path1        
    dest0x, dest0y = path0[-1]
    dest1x, dest1y = path1[-1]
    if dest0x < dest1x:
        return path0
    if dest0x > dest1x:
        return path1
    if dest0y < dest1y:
        return path0
    return path1
