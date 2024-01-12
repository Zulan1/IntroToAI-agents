from enum import Enum
from abc import ABC, abstractmethod
from grid import Grid, UpdateGridType
from type_aliases import Node, Edge

class Agent(ABC):
    """abstract class for agents

    Args:
        ABC (_type_): abstract inheritor
    """

    def __init__(self, params: list[str]) -> None:
        self._coordinates: Node = (int(params[0]), int(params[1]))
        self.done = False


    @property
    def coordinates(self) -> Node:
        """return the coordinates property

        Returns:
            Node: The start Coordinates of the Human Agent.
        """
        return self._coordinates

    @abstractmethod
    def AgentStep(self, grid: Grid) -> Edge:
        """abstract method. implemented differently in inherted classes."""

    def ProcessStep(self, grid: Grid, action: Edge = None):
        """Updates the state of the simulator's according to the step taken by the agent

        Args:
            grid (Grid): the simulator's grid
            action (Edge, optional): the action taken. Defaults to None if no-op.
        """
        if action == None: return
        self._coordinates = action[1]     
        grid.UpdateGrid(UpdateGridType.ACTION.value, action)


class AgentType(Enum):
    """Agent Type Enum"""
    GREEDY = 'A'
    HUMAN = 'H'
    INTERFERING = 'I'
