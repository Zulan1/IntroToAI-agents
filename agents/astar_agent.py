from __future__ import annotations
import copy
import heapq
import time
from typing import Tuple
from agents.search_agent import SearchAgent
from agents.interfering_agent import InterferingAgent
from agents.agent import Agent
from grid import Grid
from type_aliases import Node, Edge

State = Tuple[Grid, Agent, InterferingAgent]
ROUND_DIGITS = 5

class AStarAgent(SearchAgent):
    """class for Greedy Agent"""
    states: list[Tuple[int, int, int, State]] = []
    visitedStates: set[Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]]], Tuple[Edge]] = set()
    limit = 0
    l = 10000

    def __init__(self, params: list[str], _: Grid):
        super().__init__(params, _)
        self.cost = 0

    def FormulateGoal(self, grid: Grid, _: int) -> set[Node]:
        """Formulates the goal of the agent"""
        from heuristics import GetPickUpsAndDropDowns

        return GetPickUpsAndDropDowns(grid, self)

    def ExceededLimit(self, _: AStarAgent) -> list[Node]:
        """Checks if the agent exceeded the limit"""
        self.done = True
        return []


    def Search(self, grid: Grid, nodes: set[Node], agents: list[Agent], i: int) -> list[Node]:
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
        AStarAgent.states = []
        AStarAgent.visitedStates = set()
        AStarAgent.limit = 0
        self.cost = i

        iterations = 1
        maxT = float('-inf')
        while nextAgent.score != Grid.numOfPackages:
            st = time.time()

            if self.limit >= self.l:
                return self.ExceededLimit(nextAgent)
            self.limit += 1

            actions = set(edge[1] for edge in nextGrid.graph.edges() if edge[0] == nextAgent.coordinates)
            actions = actions.union(set(edge[0] for edge in nextGrid.graph.edges() if edge[1] == nextAgent.coordinates))
            if any(nextAgent.coordinates == p.pickupLoc and nextAgent.cost < p.pickupTime
                   for p in sum(nextGrid.packages.values(), [])):
                actions.add(nextAgent.coordinates)

            for action in actions:
                if any(nextAgent.cost > dropOffTime[1]
                       for dropOffTime in set(nextAgent.GetDropdowns()).union(nextGrid.GetDropdowns())): break
                stateAgent = copy.deepcopy(nextAgent)
                stateGrid = copy.deepcopy(nextGrid)
                stateInterference = copy.deepcopy(nextInterference)
                stateInterference.ProcessStep(stateGrid,
                                              stateInterference.AgentStep(stateGrid, None, None),
                                              stateAgent.cost)
                stateAgent.cost += 1
                stateAgent.ProcessStep(stateGrid, (nextAgent.coordinates, action), stateAgent.cost)
                stateAgent.seq.append(action)
                state = (stateGrid, stateAgent, stateInterference)
                h = SalesPersonHeursitic(stateGrid, nextNodes.union({stateAgent.coordinates}))
                f = stateAgent.cost + h
                visited = (stateAgent.coordinates, stateGrid.GetPickups(), stateAgent.GetDropdowns(),
                           stateInterference.coordinates, tuple(stateGrid.fragEdges))
                if visited in AStarAgent.visitedStates and action != nextAgent.coordinates: continue
                heapq.heappush(AStarAgent.states, (f, h, 1 / iterations, state))
                iterations += 1
                AStarAgent.visitedStates.add(visited)

            T = round(time.time() - st, ROUND_DIGITS)
            maxT = max(maxT, T)

            if not AStarAgent.states:
                print("no states left, problem might be unsolveable.")
                self.done = True
                return []

            f, h, _, nextState = heapq.heappop(AStarAgent.states)
            nextGrid: Grid = nextState[0]
            nextAgent: AStarAgent = nextState[1]
            nextInterference: InterferingAgent = nextState[2]
            nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, None)
            assert nextNodes or nextAgent.score == Grid.numOfPackages, "bug! no nodes left and not done"
            print(f"This expand took T={T} seconds, longest expansion took maxT={maxT} seconds")
            print(f'popped f: {f}, h: {h}, g: {nextAgent.cost}')
            print(f"path: {nextAgent.seq}")
            print(f"limit: {self.limit}")
            print(f"pickups: {nextGrid.GetPickups()}, dropdowns: {nextAgent.GetDropdowns()}")
            print(f"future dropdowns: {nextGrid.GetDropdowns()}")
            print(f"score: {nextAgent.score}")
            print('\n')
        return nextAgent.seq
