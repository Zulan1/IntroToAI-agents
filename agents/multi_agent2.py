from __future__ import annotations
import time
import copy
import heapq
from typing import Tuple
from type_aliases import Node, Edge
from grid import Grid
from agents.agent import Agent
from agents.astar_agent import AStarAgent
from agents.interfering_agent import InterferingAgent

ROUND_DIGITS = 5

class MultiAgent2(Agent):
    """MultiAgent class"""
    state = Tuple[Grid, Agent, InterferingAgent]
    states: list[Tuple[int, int, int, state]] = []
    visitedStates: set[Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]]], Tuple[Edge]] = set()
    limit = 0
    l = 1000000

    def __init__(self, params: list[str], _: Grid) -> None:
        super().__init__(params, _)
        self.agent1: AStarAgent = AStarAgent(params[:2], _)
        self.agent2: AStarAgent = AStarAgent(params[2:], _)

    @property
    def score(self) -> int:
        """Returns self.score"""
        return self.agent1.score + self.agent2.score

    @property
    def cost(self) -> int:
        """Returns self.cost"""
        return self.agent1.cost

    @cost.setter
    def cost(self, value: int) -> None:
        """Sets self.cost"""
        self.agent1.cost = value
        self.agent2.cost = value

    def FormulateGoal(self, grid: Grid, _: int) -> set[Node]:
        """Formulates the goal for the agent"""
        return self.agent1.FormulateGoal(grid, _).union(self.agent2.FormulateGoal(grid, _))

    def ExceededLimit(self, _: AStarAgent) -> Tuple[list[Node]]:
        """Checks if the agent exceeded the limit"""
        self.done = True
        return [], []

    def GetDropdowns(self) -> list[Tuple[Node, int]]:
        """Returns the dropdowns of the agent"""
        return self.agent1.GetDropdowns() + self.agent2.GetDropdowns()

    def AgentStep(self, grid: Grid, _: list[Agent], i: int) -> Tuple[Node]:
        noOp1 = (self.agent1.coordinates, self.agent1.coordinates)
        noOp2 = (self.agent2.coordinates, self.agent2.coordinates)

        self.agent1.ProcessStep(grid, noOp1, i)
        self.agent2.ProcessStep(grid, noOp2, i)
        if not self.agent1.seq and not self.agent2.seq:
            nodes = self.FormulateGoal(grid, i)
            if not nodes:
                self.done = True
                return noOp1, noOp2
            self.agent1.seq, self.agent2.seq = self.Search(grid, nodes, _, i)

        # Checking the validty of the propesed path
        if not self.agent1.seq and not self.agent2.seq: return noOp1, noOp2

        action1: Edge = (self.agent1.coordinates, self.agent1.seq[0]) if self.agent1.seq else noOp1
        action2: Edge = (self.agent2.coordinates, self.agent2.seq[0]) if self.agent2.seq else noOp2

        if (action1 not in grid.graph.edges() and action1[::-1] not in grid.graph.edges() and action1 != noOp1) or\
            (action2 not in grid.graph.edges() and action2[::-1] not in grid.graph.edges() and action2 != noOp2):
            self.agent1.seq, self.agent2.seq = [], []
            return self.AgentStep(grid, _, i)
        self.agent1.seq, self.agent2.seq = self.agent1.seq[1:], self.agent2.seq[1:]
        return action1, action2

    def ProcessStep(self, grid: Grid, action: Edge = None, _: int = 0):
        if not action:
            action = ((self.agent1.coordinates, self.agent1.coordinates),
                      (self.agent2.coordinates, self.agent2.coordinates))
        self.agent1.ProcessStep(grid, action[0], _)
        self.agent2.ProcessStep(grid, action[1], _)

    def Search(self, grid: Grid, nodes: set[Node], agents: list[Agent], i: int) -> Tuple[list[Node]]:
        """Searches for the goal"""
        from heuristics import MultiAgentHeuristic2
        from utils import Dijkstra

        nextGrid: Grid = grid
        nextAgent: MultiAgent2 = self
        nextNodes: set[Node] = nodes

        nextInterference: InterferingAgent = [agent for agent in agents if isinstance(agent, InterferingAgent)][0]
        MultiAgent2.limit = 0
        MultiAgent2.states = []
        MultiAgent2.visitedStates = set()
        self.cost = i
        iterations = 1
        listT = []
        maxT = float('-inf')

        while nextAgent.score != Grid.numOfPackages:
            st = time.time()
            if self.limit >= self.l:
                return self.ExceededLimit(nextAgent)
            self.limit += 1

            def GetActions(fAgent: AStarAgent, fGrid: Grid) -> set[Node]:
                if (not fGrid.GetPickups() and not fAgent.packages): return {fAgent.coordinates}
                actions = set(edge[1] for edge in fGrid.graph.edges() if edge[0] == fAgent.coordinates)\
                    .union(set(edge[0] for edge in fGrid.graph.edges() if edge[1] == fAgent.coordinates))
                if any(len(Dijkstra(fGrid.graph, fAgent.coordinates, p.pickupLoc)) - 1 < p.pickupTime - fAgent.cost
                       for p in sum(fGrid.packages.values(), [])):
                    print(f"Agent is at {fAgent.coordinates} and might need to wait")
                    actions.add(fAgent.coordinates)
                return actions
            actions1 = GetActions(nextAgent.agent1, nextGrid)
            actions2 = GetActions(nextAgent.agent2, nextGrid)

            for action1 in actions1:
                for action2 in actions2:
                    if any(nextAgent.cost > dropOffTime[1]
                       for dropOffTime in set(nextAgent.agent1.GetDropdowns()).union(
                           set(nextAgent.agent2.GetDropdowns()).union(nextGrid.GetDropdowns()))): break
                    stateAgent = copy.deepcopy(nextAgent)
                    stateGrid = copy.deepcopy(nextGrid)
                    stateInterference = copy.deepcopy(nextInterference)
                    stateInterference.ProcessStep(stateGrid,
                                                  stateInterference.AgentStep(stateGrid, None, None), stateAgent.cost)
                    stateAgent.cost += 1
                    stateAgent.ProcessStep(stateGrid,
                                           ((stateAgent.agent1.coordinates, action1),
                                            (stateAgent.agent2.coordinates, action2)),
                                           stateAgent.cost)
                    stateAgent.agent1.seq.append(action1)
                    stateAgent.agent2.seq.append(action2)
                    visited = (stateGrid.GetPickups(),
                               (stateAgent.agent1.coordinates, stateAgent.agent1.GetDropdowns()),
                               (stateAgent.agent2.coordinates, stateAgent.agent2.GetDropdowns()),
                               stateInterference.coordinates, tuple(stateGrid.fragEdges))
                    state = (stateGrid, stateAgent, stateInterference)
                    h = MultiAgentHeuristic2(stateGrid, stateAgent, stateAgent.cost)
                    f = stateAgent.cost + h
                    if stateAgent.agent2.coordinates == nextAgent.agent2.coordinates == (1, 3):
                        print(f"nextNodes: {nextNodes}")
                        print(f"h: {h}, f: {f}" + '\n'*10)
                    if visited in MultiAgent2.visitedStates and\
                    (action1 != nextAgent.agent1.coordinates or action2 != nextAgent.agent2.coordinates): continue
                    heapq.heappush(MultiAgent2.states, (f, h, 1 / iterations, state))
                    iterations += 1
                    MultiAgent2.visitedStates.add(visited)

            T = round(time.time() - st, ROUND_DIGITS)
            listT.append(T)
            maxT = max(maxT, T)

            if not MultiAgent2.states:
                print("no states left, problem might be unsolveable.")
                self.done = True
                return [], []

            f, h, _, nextState = heapq.heappop(MultiAgent2.states)
            nextGrid: Grid = nextState[0]
            nextAgent: MultiAgent2 = nextState[1]
            nextInterference: InterferingAgent = nextState[2]
            nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, None)
            assert nextNodes or nextAgent.GetDropdowns() or nextAgent.score == Grid.numOfPackages,\
            "bug! no nodes left and not done"
        print(f"This expand took T={T} seconds, longest expansion took maxT={maxT} seconds")
        print(f"avg listT={round(sum(listT) / len(listT), ROUND_DIGITS)} seconds, Total time: {sum(listT)} seconds")
        print(f'popped f: {f}, h: {h}, g: {nextAgent.cost}')
        print(f"path1: {nextAgent.agent1.seq}\npath2: {nextAgent.agent2.seq}")
        print(f"limit: {self.limit}")
        print(f"pickups: {nextGrid.GetPickups()}")
        print(f"dropdowns1: {nextAgent.agent1.GetDropdowns()}, dropdowns2: {nextAgent.agent2.GetDropdowns()}")
        print(f"future dropdowns: {nextGrid.GetDropdowns()}")
        print(f"score1: {nextAgent.agent1.score}, score2: {nextAgent.agent2.score}")
        print('\n')
        print(f"total time: {round(sum(listT), ROUND_DIGITS)} seconds")
        print(f"chosen path1: {nextAgent.agent1.seq}\nchosen path2: {nextAgent.agent2.seq}")
        return nextAgent.agent1.seq, nextAgent.agent2.seq
