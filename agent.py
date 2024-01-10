from abc import ABC, abstractmethod
from enum import Enum

class Agent(ABC):
    """abstract class for agents

    Args:
        ABC (_type_): abstract inheritor
    """

    @abstractmethod
    def AgentStep(self):
        """do nothing
        """

class AgentType(Enum):
    """Agent Type Enum
    """
    GREEDY = 'A'
    HUMAN = 'H'
    INTERFERING = 'I'
