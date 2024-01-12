from grid import Grid, UpdateGridType
from agent import Agent, AgentType
# from greedy_agent import GreedyAgent
from human_agent import HumanAgent
from interfering_agent import InterferingAgent

def InitGrid(initFilePath: str) -> (Grid, list[Agent]):
    """initializes grid from init file

    Args:
        initFilePath (str): init file path

    Returns:
        Grid: Simulator's grid
        list[Agent]: the agents activated in the simulator
    """
    with open(initFilePath, 'r') as f:
        lines = list(line.split(';')[0].split('#')[1].strip().split(' ')
                     for line in f.readlines() if line.startswith("#"))
        lines = list(list(filter(lambda e: e!='', line)) for line in lines)

    x = list(int(line[1]) for line in lines if line[0].lower() == 'x')[0]
    y = list(int(line[1]) for line in lines if line[0].lower() == 'y')[0]
    grid: Grid = Grid(x, y)

    for line in lines:
        action = line[0]
        if any(action == updateGridType.value for updateGridType in UpdateGridType):
            grid.UpdateGrid(action, line[1:])

    agents = list()
    for line in lines:
        action = line[0]
        if not any(action == agentType.value for agentType in AgentType): continue
        # if action == AgentType.GREEDY.value:
        #     agents.append(GreedyAgent(line[1:]))
        if action == AgentType.HUMAN.value:
            agents.append(HumanAgent(line[1:], grid))
        if action == AgentType.INTERFERING.value:
            agents.append(InterferingAgent(line[1:]))

    return grid, agents
