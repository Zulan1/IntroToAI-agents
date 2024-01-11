from abc import ABC, abstractmethod
from enum import Enum

class Agent(ABC):
    """abstract class for agents

    Args:
        ABC (_type_): abstract inheritor
    """

    def __init__(self, params: list[str]) -> None:
        self.startCoords: (int, int) = (params[0], params[1])
    
    @abstractmethod
    def AgentStep(self):
        """do nothing
        """
    
    @property
    def startCoords(self) -> (int, int):
        """return the startCoords property

        Returns:
            (int, int): The start Coordinates of the Human Agent.
        """
        return self.startCoords
    
class AgentType(Enum):
    """Agent Type Enum
    """
    GREEDY = 'A'
    HUMAN = 'H'
    INTERFERING = 'I'
