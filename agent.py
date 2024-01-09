from abc import ABC, abstractmethod

class Agent(ABC):
    """abstract class for agents

    Args:
        ABC (_type_): abstract inheritor
    """

    @abstractmethod
    def AgentStep(self):
        """do nothing
        """
