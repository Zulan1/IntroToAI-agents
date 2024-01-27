from __future__ import annotations
import copy
import heapq
import time
from typing import Tuple
from agents.search_agent import SearchAgent
from agents.interfering_agent import InterferingAgent
from agents.agent import Agent
from grid import Grid
from type_aliases import Node

State = Tuple[Grid, SearchAgent]

class AStarAgent(SearchAgent):
    """class for Greedy Agent"""
    states: list[Tuple[int, int, int, int, State]] = []
    limit = 10000

    def __init__(self, params: list[str]):
        super().__init__(params)
        self.cost = 0

    def FormulateGoal(self, grid: Grid, _: int) -> set[Node]:
        """Formulates the goal of the agent"""
        from heuristics import GetPickUpsAndDropDowns

        return GetPickUpsAndDropDowns(grid, self)

    def ExceededLimit(self, _: AStarAgent) -> list[Node]:
        """Checks if the agent exceeded the limit"""
        print(self.limit)
        self.done = True
        AStarAgent.states = []
        return []


    def Search(self, grid: Grid, nodes: set[Node], agents: list[Agent], _: int) -> list[Node]:
        """Searches for the shortest path to the goal

        Args:
            grid (Grid): the simulator's grid
            nodes (set[Node]): the goal

        Returns:
            list[Node]: the shortest path to the goal
        """
        from heuristics import SalesPersonHeursitic

        nextGrid: Grid = grid
        nextAgent: AStarAgent = self
        nextNodes: set[Node] = nodes
        nextInterference: InterferingAgent = [agent for agent in agents if isinstance(agent, InterferingAgent)][0]

        while nextAgent.score != Grid.numOfPackages:

            actions = set(edge[1] for edge in grid.graph.edges() if edge[0] == nextAgent.coordinates)
            actions = actions.union(set(edge[0] for edge in grid.graph.edges() if edge[1] == nextAgent.coordinates))
            if not nextGrid.FilterAppearedPackages(nextAgent.cost):
                actions.add(nextAgent.coordinates)

            if self.limit <= 0:
                return self.ExceededLimit(nextAgent)
            self.limit -= 1

            for action in actions:
                stateAgent = copy.deepcopy(nextAgent) # coordinates, done, seq, pack, score, cost, limit, states
                stateGrid = copy.deepcopy(nextGrid) # size, graph, packages, fragEdges
                stateInterference = copy.deepcopy(nextInterference)
                stateInterference.ProcessStep(stateGrid, stateInterference.AgentStep(stateGrid, None, None), stateAgent.cost)
                stateAgent.cost += 1
                stateAgent.ProcessStep(stateGrid, (nextAgent.coordinates, action), stateAgent.cost)
                stateAgent.seq.append(action)
                state = (stateGrid, stateAgent, stateInterference)
                h = SalesPersonHeursitic(stateGrid, nextNodes.union({stateAgent.coordinates}))
                f = stateAgent.cost + h
                heapq.heappush(AStarAgent.states, (f, action[0], action[1], time.time(), state))

            nextState = heapq.heappop(AStarAgent.states)[4]
            nextGrid: Grid = nextState[0]
            nextAgent: AStarAgent = nextState[1]
            nextInterference: InterferingAgent = nextState[2]
            nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, stateAgent.cost)
            # print(f'popped f: {f}, h: {f - nextAgent.cost} g: {nextAgent.cost}')
            # print(f"path: {nextAgent.seq}")
            # print(f"limit: {self.limit}")
            # print(nextNodes)
            # print('\n')
        return nextAgent.seq
