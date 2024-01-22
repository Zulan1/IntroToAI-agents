import os
import configparser
from os import path
from agent import Agent
from grid import Grid
from utils import InitGrid
from human_agent import HumanAgent
from search_agent import SearchAgent


def Main():
    """Main function of the project
    Args:
        argc (int): System Arguments Count
        argv (list[str]): System Arguments
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    filePath = config['settings']['grid_config_path']
    assert filePath, "Path to grid configuration file is not specified!"
    assert path.exists(filePath), "Path to grid configuration file does not exist!"

    grid: Grid
    agents: list[Agent]
    grid, agents = InitGrid(filePath)

    i = 0
    while any(agent.done is not True for agent in agents):
        for agent in agents:
            if isinstance(agent, SearchAgent):
                action = agent.AgentStep(grid, i)
                agent.ProcessStep(grid, action, i)
            else:
                if isinstance(agent, HumanAgent):
                    action = agent.AgentStep(grid, agents, i)
                else:
                    action = agent.AgentStep(grid)
                agent.ProcessStep(grid, action)
        i += 1

if __name__ == "__main__":
    Main()
