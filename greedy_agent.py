# import copy
from typing import Tuple
from search_agent import SearchAgent
from grid import Grid
from type_aliases import Node

class GreedyAgent(SearchAgent):
    """class for Greedy Agent"""

    def __init__(self, params: list[str]):
        super().__init__(params)
        self.visitedStates: set[Tuple[Grid, self]] = set()

    def FormulateGoal(self, grid: Grid, i: int) -> set[Node]:
        """Formulates the goal of the agent"""
        from heuristics import GetPickUpsAndDropDowns

        # todo: correct this algorithm
        # # Check if all properties of grid and agent match all properties of a visited state
        # print(grid.__dict__.values(), '\n', self.__dict__.values(), '\n\n')
        # for g, a in self.visitedStates:
        #     print(g.__dict__.values(), '\n', a.__dict__.values(), '\n\n')
        # if self.visitedStates and all(value1 == value2 for state in self.visitedStates
        #        for value1, value2 in zip(grid.__dict__.values(), state[0].__dict__.values())) and\
        #            all(value1 == value2 for state in self.visitedStates
        #                for value1, value2 in zip(self.__dict__.values(), state[1].__dict__.values())):
        #     return set()
        # self.visitedStates.add((copy.copy(grid), copy.copy(self)))

        return GetPickUpsAndDropDowns(grid, self)

    def Search(self, grid: Grid, nodes: set[Node]) -> list[Node]:
        """Searches for the shortest path to the goal

        Args:
            grid (Grid): the simulator's grid
            nodes (set[Node]): the goal

        Returns:
            list[Node]: the shortest path to the goal
        """
        from heuristics import SalesPersonHeursitic

        actions = set(edge[1] for edge in grid.graph.edges() if edge[0] == self.coordinates)
        actions = actions.union(set(edge[0] for edge in grid.graph.edges() if edge[1] == self.coordinates))

        return [min(actions, key=lambda action: SalesPersonHeursitic(grid, nodes.union({action})))]
