from agent import Agent
from grid import Grid

class HumanAgent(Agent):
    """class for Human Agent
    """

    def __init__(self, grid: Grid, params: list[str]):
        self.grid = grid
        self.startCoords: (int, int) = (params[0], params[1])

    @property
    def startCoords(self) -> (int, int):
        """return the startCoords property

        Returns:
            (int, int): The start Coordinates of the Human Agent.
        """
        return self.startCoords

    def AgentStep(self) -> (int, int):
        """Calculates the next step of the Human Agent

        Returns:
            (int, int): The Coordinates the Human agent goes to in the next step.
        """
        super().AgentStep()
        
