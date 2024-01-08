import sys
from os import path
from grid import Grid
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

    grid, agents = InitGrid(filePath)
    
    while True:
        for agent in agents:
            if agent[0] == 'A':
                # run normal agent
            if agent[0] == 'H':
                # run human agent
            if agent[0] == 'I':
                # run interfering agent

if __name__ == "__main__":
    Main(sys.argc, sys.argv)
