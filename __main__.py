import configparser
from os import path
from grid import Grid
from utils import InitGrid
from agents.agent import Agent
from agents.astar_agent import AStarAgent
from agents.rtastar_agent import RTAStarAgent


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

    i = 0
    while any(agent.done is not True for agent in agents) and i <= Agent.lastDropOffTime:
        for agent in agents:
            action = agent.AgentStep(grid, agents, i)
            agent.ProcessStep(grid, action, i)
        i += 1

if __name__ == "__main__":
    Main()
