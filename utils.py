from grid import Grid, UpdateGridType
from agent import AgentType
from greedy_agent import GreedyAgent
from human_agent import HumanAgent
from interfering_agent import InterferingAgent

def InitGrid(initFilePath: str) -> (list[list[str]]):
    """initializes grid from init file

    Args:
        initFilePath (str): init file path

    Returns:
        Grid: Simulator's grid
    """
    with open(initFilePath, 'r') as f:
        lines = list(line.split(';')[0].split('#')[1].strip().split(' ') for line in f.readlines() if line.startswith("#"))
        lines = list(list(filter(lambda e: e!='', line)) for line in lines)

    x = list(int(line[1]) for line in lines if line[0].lower() == 'x')[0]
    y = list(int(line[1]) for line in lines if line[0].lower() == 'y')[0]

    grid = Grid(x, y)
    for line in lines:
        updateGridType = line[0]
        if updateGridType not in UpdateGridType: continue
        grid.UpdateGrid(line[0], line[1:])

    agents = list()
    for line in lines:
        agentType = line[0]
        if agentType not in AgentType: continue
        if agentType == AgentType.GREEDY:
            agents.append(GreedyAgent(grid, line[1:]))
        if agentType == AgentType.HUMAN:
            agents.append(HumanAgent(grid, line[1:]))
        if agentType == AgentType.INTERFERING:
            agents.append(InterferingAgent(grid, line[1:]))


    return agents
