from __future__ import annotations
import heapq
from type_aliases import Node
from grid import Grid
from agents.multi_agent import MultiAgent, MultiAgentState

ROUND_DIGITS = 5

class MultiAgent2(MultiAgent):
    """MultiAgent2 class"""
    l = 1000000

    def HeapPush(self, states: list[int, int, int, int, MultiAgentState], grid: Grid,
                iterations: list[int], nodes: set[Node], currentState: MultiAgentState) -> None:
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
        heapq.heappush(states, (f, h, 0, 1 / iterations[0], currentState, nodes, nodes))
        iterations[0] += 1
