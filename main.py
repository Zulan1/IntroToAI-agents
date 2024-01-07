import sys
from os import path

def Main(argc: int, argv: list[str]):
    """Main function of the project
    Args:
        argc (int): System Arguments Count
        argv (list[str]): System Arguments
    """
    assert argc >= 2, "Arg1 should be the path to grid configuration file"
    filePath = argv[1]
    assert path.exists(filePath), "Path to grid configuration file does not exist!"

    with open(filePath, 'r') as f:
        lines = list(line.split('#')[0] for line in f.readlines())
    
    grid: Grid = 


if __name__ == "__main__":
    Main(sys.argc, sys.argv)
