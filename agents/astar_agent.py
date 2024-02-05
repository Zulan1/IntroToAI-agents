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

    def GetActions(self, grid: Grid) -> set[Node]:
        """
        Returns a set of possible actions for the agent based on the current grid state.

        Parameters:
        grid (Grid): The grid representing the current state of the environment.

        Returns:
        set[Node]: A set of possible actions for the agent.
        """
        from utils import GetNeighbors

        actions = GetNeighbors(grid, self.coordinates)
        if any(self.coordinates == p.pickupLoc and self.cost < p.pickupTime
                for p in sum(grid.packages.values(), [])):
            print(f"Agent is at {self.coordinates} and might need to wait")
            actions.add(self.coordinates)
        return actions


    def Search(self, grid: Grid, nodes: set[Node], agents: list[Agent], i: int) -> list[Node]:
        """Searches for the shortest path to the goal

        Args:
            grid (Grid): the simulator's grid
            nodes (set[Node]): the goal

        Returns:
            list[Node]: the shortest path to the goal
        """
        from heuristics import SalesPersonHeursitic

        # initiallization of the state
        nextGrid: Grid = grid
        nextAgent: AStarAgent = self
        nextNodes: set[Node] = nodes
        nextInterference: InterferingAgent = [agent for agent in agents if isinstance(agent, InterferingAgent)][0]
        states: list[Tuple[int, int, int, State]] = []
        visitedStates: set[Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]], Tuple[Edge]]] = set()
        limit = 0
        listT = []
        self.cost = i
        iterations = 1
        maxT = float('-inf')

        # main loop of expanding the states of the a* algorithm
        while nextAgent.score != Grid.numOfPackages:
            st = time.time()

            # add count to limit and call handler if limit is exceeded
            if limit >= self.l:
                return self.ExceededLimit(nextAgent)
            limit += 1

            # possible nodes to move to
            actions = nextAgent.GetActions(nextGrid)

            # iterate over the possible actions i.e. expand this node
            for action in actions:
                # if any package is already expired, no point in expanding the state
                if any(nextAgent.cost > dropOffTime[1]
                       for dropOffTime in set(nextAgent.GetDropdowns()).union(nextGrid.GetDropdowns())): break

                # create deep copies of agents so we don't affect the current state
                stateAgent = copy.deepcopy(nextAgent)
                stateGrid = copy.deepcopy(nextGrid)
                stateInterference = copy.deepcopy(nextInterference)

                # process the next state
                stateInterference.ProcessStep(stateGrid,
                                              stateInterference.AgentStep(stateGrid, None, None),
                                              None)
                stateAgent.cost += 1
                stateAgent.ProcessStep(stateGrid, (nextAgent.coordinates, action), stateAgent.cost)
                stateAgent.seq.append(action)

                # create the state tuple and add it to the heap
                state = (stateGrid, stateAgent, stateInterference)

                # calculate the heuristic and the f value
                h = SalesPersonHeursitic(stateGrid, nextNodes.union({stateAgent.coordinates}))
                f = stateAgent.cost + h

                # check if the current move mwas already tried in the exact same state
                visited = (stateAgent.coordinates,
                           stateGrid.GetPickups(), stateAgent.GetDropdowns(),
                           tuple(stateGrid.fragEdges))
                if visited in visitedStates and action != nextAgent.coordinates: continue

                # add the state to the heap prio lower f value then lower h value then lifo (arbitrary)
                heapq.heappush(states, (f, h, 1 / iterations, state))
                iterations += 1
                visitedStates.add(visited)

            # check how long this node expansion took
            T = round(time.time() - st, ROUND_DIGITS)
            listT.append(T)
            maxT = max(maxT, T)

            # in case every node was visited and the state didn't change so problem is probably unsolveable
            if not states:
                print("no states left, problem might be unsolveable.")
                self.done = True
                return []

            # pop the next state and setup for the next iteration
            f, h, _, nextState = heapq.heappop(states)
            nextGrid: Grid = nextState[0]
            nextAgent: AStarAgent = nextState[1]
            nextInterference: InterferingAgent = nextState[2]
            nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, None)

            # should not reach here, if there's no pickups nor dropoffs then the agent should be done
            assert nextNodes or nextAgent.score == Grid.numOfPackages, "bug! no nodes left and not done"

        # some debug info
        print(f"This expand took T={T} seconds, longest expansion took maxT={maxT} seconds")
        print(f"avg listT={round(sum(listT) / len(listT), ROUND_DIGITS)} seconds, Total time: {sum(listT)} seconds")
        print(f'popped f: {f}, h: {h}, g: {nextAgent.cost}')
        print(f"path: {nextAgent.seq}")
        print(f"limit: {limit}")
        print(f"pickups: {nextGrid.GetPickups()}, dropdowns: {nextAgent.GetDropdowns()}")
        print(f"future dropdowns: {nextGrid.GetDropdowns()}")
        print(f"score: {nextAgent.score}")
        print('\n')
        return nextAgent.seq
