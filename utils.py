from grid import Grid

def InitGrid(initFilePath: str) -> (Grid, list[list[str]]):
    """initializes grid from init file

    Args:
        initFilePath (str): init file path

    Returns:
        Grid: Simulator's grid
    """
    with open(initFilePath, 'r') as f:
        lines = list(line.split(';')[0].split('#')[1].strip().split(' ') for line in f.readlines())

    x = list(int(line[1]) for line in lines if line[0].lower() == 'x')[0]
    y = list(int(line[1]) for line in lines if line[0].lower() == 'y')[0]

    grid = Grid(x, y)
    updateGridCmds = {'B', 'P', 'F'}
    agentsCmds = {'A', 'H', 'I'}
    agents = list(line for line in lines if line[0] in agentsCmds)
    for line in lines:
        if line[0] in updateGridCmds:
            grid.UpdateGrid(line[0], line[1:])

    return grid, agents
