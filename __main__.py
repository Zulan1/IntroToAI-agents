import configparser
from os import path
from grid import Grid
from utils import InitGrid
from agents.agent import Agent
from agents.human_agent import HumanAgent
from agents.search_agent import SearchAgent
from agents.interfering_agent import InterferingAgent


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
    #interfereingAgent = [a for a in agents if isinstance(a, InterferingAgent)][0]
    i = 0
    while any(agent.done is not True for agent in agents):
        for agent in agents:
            if isinstance(agent, SearchAgent):
                action = agent.AgentStep(grid, i)#, interfereingAgent
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
