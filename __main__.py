import configparser
from os import path
from grid import Grid
from utils import InitGrid
from agents.agent import Agent
from agents.human_agent import HumanAgent
from agents.search_agent import SearchAgent
from agents.astar_agent import AStarAgent
from agents.rtastar_agent import RTAStarAgent
from agents.interfering_agent import InterferingAgent


def Main():
    """Main function of the project
    Args:
        argc (int): System Arguments Count
        argv (list[str]): System Arguments
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    filePath = config['settings'].get('grid_config_path', './tests/test1.txt')
    assert path.exists(filePath), "Path to grid configuration file does not exist!"

    limit = int(config['settings'].get('limit', 10000))
    l = int(config['settings'].get('L', 10))
    AStarAgent.l = limit
    RTAStarAgent.l = l

    grid: Grid
    agents: list[Agent]
    grid, agents = InitGrid(filePath)
    lastDropOffTime = max(p.dropOffMaxTime for p in sum(grid.packages.values(), []))
    # interfereingAgent = [a for a in agents if isinstance(a, InterferingAgent)][0]
    # humanAgent = [a for a in agents if isinstance(a, HumanAgent)][0]
    # otherAgents = [a for a in agents if not isinstance(a, HumanAgent)]

    i = 0
    while any(agent.done is not True for agent in agents) and i <= lastDropOffTime:
        for agent in agents:
            action = agent.AgentStep(grid, agents, i)
            agent.ProcessStep(grid, action, i)
        i += 1

if __name__ == "__main__":
    Main()
