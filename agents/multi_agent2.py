from __future__ import annotations
import heapq
from typing import Tuple
from type_aliases import Node
from grid import Grid
from agents.agent import Agent
from agents.multi_agent import MultiAgent
from agents.astar_agent import State
from agents.interfering_agent import InterferingAgent

State = Tuple[Grid, Agent, InterferingAgent]
ROUND_DIGITS = 5

class MultiAgent2(MultiAgent):
    """MultiAgent2 class"""
    l = 1000000

    def HeapPush(self, states: list[int, int, int, int, State], grid: Grid, interfering: InterferingAgent,
                iterations: list[int], nodes: set[Node]) -> None:
        """
        Pushes a state onto the heap.

        Args:
            states (list[int, int, int, int, State]): The list of states.
            state (State): The state to push onto the heap.
            iterations (list[int]): The list of iteration counts.
            visited (Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]]]): The visited state.
            visitedStates (set[Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]]], Tuple[Edge]]): 
                The set of visited states.

        Returns:
            None
        """
        from heuristics import MultiAgentHeuristic2

        h = MultiAgentHeuristic2(grid, self, self.cost)
        f = self.cost + h

        # save the new states to the heap
        state = (grid, self, interfering)
        heapq.heappush(states, (f, h, 0, 1 / iterations[0], state, nodes, nodes))
        iterations[0] += 1
