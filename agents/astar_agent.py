from __future__ import annotations
import copy
import heapq
import time
from typing import Tuple
from agents.search_agent import SearchAgent
from agents.interfering_agent import InterferingAgent
from grid import Grid
from type_aliases import Node

State = Tuple[Grid, SearchAgent]
LIMIT = 975

class AStarAgent(SearchAgent):
    """class for Greedy Agent"""
    states: list[Tuple[int, int, int, int, State]] = []

    def __init__(self, params: list[str]):
        super().__init__(params)
        self.cost = 0
        self.limit = LIMIT

    def FormulateGoal(self, grid: Grid, _: int) -> set[Node]:
        """Formulates the goal of the agent"""
        from heuristics import GetPickUpsAndDropDowns

        return GetPickUpsAndDropDowns(grid, self)

<<<<<<< HEAD
    def Search(self, grid: Grid, nodes: set[Node], i: int, root: SearchAgent = None) -> list[Node]: #, interference: InterferingAgent
=======
    def Search(self, grid: Grid, nodes: set[Node], i: int, root: AStarAgent = None) -> list[Node]:
>>>>>>> c9cfc2f34aaf74a379e522284f4e40223a95c09a
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
        root = root or self

        if not nodes:
            return self.seq

        root.limit -= 1
        if root.limit <= 1:
            # root.done = True
            root.limit = LIMIT
            AStarAgent.states = []
            return []

        for action in actions:
            stateAgent = copy.deepcopy(self) # coordinates, done, seq, pack, score, cost, limit, states
            stateGrid = copy.deepcopy(grid) # size, graph, packages, fragEdges
            # stateInterference = copy.deepcopy(interference) 
            # stateInterference.ProcessStep(stateGrid, stateInterference.AgentStep(stateGrid))            
            stateAgent.ProcessStep(stateGrid, (self.coordinates, action), i + 1)
            stateAgent.cost += 1
            stateAgent.seq.append(action)
            state = (stateGrid, stateAgent)
            h = SalesPersonHeursitic(stateGrid, nodes.union({stateAgent.coordinates}))
            f = stateAgent.cost + h
            heapq.heappush(AStarAgent.states, (f, action[0], action[1], time.time(), state))

        nextState = heapq.heappop(AStarAgent.states)[4]
        nextGrid: Grid = nextState[0]
        nextAgent: SearchAgent = nextState[1]
        nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, i + 1)
        # print(f'popped f: {f}, h: {f - nextAgent.cost} g: {nextAgent.cost}')
        # print(f"path: {nextAgent.seq}")
        # print(f"node: ({x}, {y})")
        # print(f"limit: {root.limit}")
        # print(nextNodes)
        # print('\n')
        return nextAgent.Search(nextGrid, nextNodes, i + 1, root) #, stateInterference
