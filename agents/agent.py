from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from grid import Grid, UpdateGridType
from type_aliases import Node, Edge

class Agent(ABC):
    """abstract class for agents

    Args:
        ABC: inherits from abstract class
    """
    lastDropOffTime: int = float('inf')

    def __init__(self, params: list[str], _: Grid) -> None:
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
    def AgentStep(self, grid: Grid, agents: list[Agent], i: int) -> Edge:
        """abstract method. implemented differently in inherted classes."""

    def ProcessStep(self, grid: Grid, action: Edge = None, _: int = 0):
        """Updates the state of the simulator's according to the step taken by the agent

        Args:
            grid (Grid): the simulator's grid
            action (Edge, optional): the action taken. Defaults to None if no-op.
        """
        if action is None: return
        self._coordinates = action[1]
        grid.UpdateGrid(UpdateGridType.ACTION.value, action)


class AgentType(Enum):
    """Agent Type Enum"""
    STUPID_GREEDY = 'SG'
    GREEDY = 'G'
    A_STAR = 'A'
    RTA_STAR = 'RTA'
    HUMAN = 'H'
    INTERFERING = 'I'
