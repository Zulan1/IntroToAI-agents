from agent import Agent
from grid import Grid

class HumanAgent(Agent):
    """class for Human Agent
    """

    def __init__(self, params: list[str]):
        super().__init__(params)
        


    def AgentStep(self) -> (int, int):
        """Calculates the next step of the Human Agent

        Returns:
            (int, int): The Coordinates the Human agent goes to in the next step.
        """
        super().AgentStep()
                
