import sys
import time
from os import path
from agent import Agent
from grid import Grid
from utils import InitGrid, HumanAgent, GreedyAgent

def Main(argc: int, argv: list[str]):
    """Main function of the project
    Args:
        argc (int): System Arguments Count
        argv (list[str]): System Arguments
    """
    assert argc >= 2, "Arg1 should be the path to grid configuration file"
    filePath = argv[1]
    assert path.exists(filePath), "Path to grid configuration file does not exist!"

    grid: Grid
    agents: list[Agent]
    grid, agents = InitGrid(filePath)

    i = 0
    while any(agent.done is not True for agent in agents):
        st = time.time()
        for agent in agents:
            if isinstance(agent, GreedyAgent):
                action = agent.AgentStep(grid, i)
                agent.ProcessStep(grid, action, i)
            else:
                if isinstance(agent, HumanAgent):
                    action = agent.AgentStep(grid, agents, i)
                else:
                    action = agent.AgentStep(grid)
                agent.ProcessStep(grid, action)
        while time.time() - st < 2:
            pass
        i += 1

if __name__ == "__main__":
    Main(len(sys.argv), sys.argv)
