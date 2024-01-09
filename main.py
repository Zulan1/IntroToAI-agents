import sys
from os import path
from grid import Grid
from agent import Agent
from utils import InitGrid

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
    
    while True:
        for agent in agents:
            agent.AgentStep()

if __name__ == "__main__":
    Main(sys.argc, sys.argv)
