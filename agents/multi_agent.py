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

class MultiAgent(Agent):
    """MultiAgent class"""
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
        gridPickupdsAndDropdowns = set((p[0], d[0]) for p, d in zip(grid.GetPickups(), grid.GetDropdowns()))
        return set(gridPickupdsAndDropdowns)

    def ExceededLimit(self, _: AStarAgent) -> Tuple[list[Node]]:
        """Checks if the agent exceeded the limit"""
        self.done = True
        return [], []

    def GetDropdowns(self) -> list[Tuple[Node, int]]:
        """Returns the dropdowns of the agent"""
        return self.agent1.GetDropdowns() + self.agent2.GetDropdowns()

    def GetActions(self, grid: Grid, nodes: Tuple[set[Node]]) -> Tuple[set[Node]]:
        """
        Get the actions for the multi-agent based on the current grid and nodes.

        Args:
            grid (Grid): The current grid.
            nodes (Tuple[set[Node]]): The nodes representing the packages.

        Returns:
            Tuple[set[Node]]: The actions for each agent.
        """

        actions1 = self.agent1.GetActions(grid)\
            if (nodes[0] or self.agent1.packages) else {self.agent1.coordinates}
        actions2 = self.agent2.GetActions(grid)\
            if (nodes[1] or self.agent2.packages) else {self.agent2.coordinates}

        if actions1 == {self.agent1.coordinates} or actions2 == {self.agent2.coordinates}:
            return actions1, actions2

        neighborEdge = (self.agent1.coordinates, self.agent2.coordinates)
        if neighborEdge in grid.graph.edges or neighborEdge[::-1] in grid.graph.edges():
            actions1.add(self.agent1.coordinates)
            actions2.add(self.agent2.coordinates)

        return actions1, actions2

    def AgentStep(self, grid: Grid, _: list[Agent], i: int) -> Tuple[Node]:
        # same as agent step in search agent just for 2 agents
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

    def Expand(self, grid: Grid, interfering: InterferingAgent, nodes: set[Node], iterations: list[int],
               actions: set[Node], states: list[Tuple[int, int, int, MultiAgentState]],
               visitedStates: dict[MultiAgentState, int]) -> None:
        """
        Expands the current state by generating new states based on possible actions of the agents.

        Args:
            grid (Grid): The grid representing the environment.
            interfering (InterferingAgent): The interfering agent.
            nodes (set[Node]): The set of nodes in the grid.
            iterations (list[int]): The list of iteration counts.
            actions (set[Node]): The set of possible actions for the agents.
            states (list[Tuple[int, int, int, State]]): The list of states.
            visitedStates (set[Tuple[Node, Tuple[Tuple[Node, int]], Tuple[Tuple[Node, int]], Tuple[Edge]]]): 
                The set of visited states.

        Returns:
            None
        """
        actions1, actions2 = actions
        for action1 in actions1:
            for action2 in actions2:
                # if any package can not be delievered anymore no reason to expand
                if any(self.cost > dropOffTime[1]
                    for dropOffTime in set(self.agent1.GetDropdowns()).union(
                        set(self.agent2.GetDropdowns()).union(grid.GetDropdowns()))): break

                if ((self.agent1.coordinates, action1) == (self.agent2.coordinates, action2) or\
                    (self.agent1.coordinates, action1) == (action2, self.agent2.coordinates)) and not\
                        (action1 == self.agent1.coordinates or actions2 == self.agent2.coordinates): continue

                # deep copy to simulate without changing other states
                stateAgent = copy.deepcopy(self)
                stateGrid = copy.deepcopy(grid)
                stateInterference = copy.deepcopy(interfering)
                stateInterference.ProcessStep(stateGrid,
                                                stateInterference.AgentStep(stateGrid, None, None), stateAgent.cost)
                stateAgent.cost += 1
                stateAgent.ProcessStep(stateGrid,
                                        ((stateAgent.agent1.coordinates, action1),
                                        (stateAgent.agent2.coordinates, action2)),
                                        stateAgent.cost)
                stateAgent.agent1.seq.append(action1)
                stateAgent.agent2.seq.append(action2)

                # check if action1 + action2 changed anything in the state
                currentState = MultiAgentState(stateGrid, stateAgent, stateInterference)

                if currentState in visitedStates and visitedStates[currentState] <= stateAgent.cost and\
                (action1, action2) != (self.agent1.coordinates, self.agent2.coordinates): continue

                stateAgent.HeapPush(states, stateGrid, iterations, nodes, currentState)

                visitedStates[currentState] = stateAgent.cost

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
        from heuristics import MultiAgentHeuristic1

        maxH, minH, nodes1, nodes2 = MultiAgentHeuristic1(grid,
                                        tuple((set(d[0] for d in self.agent1.GetDropdowns())
                                            .union({self.agent1.coordinates}),
                                        set(d[0] for d in self.agent2.GetDropdowns())
                                        .union({self.agent2.coordinates}))), nodes)
        f = self.cost + maxH

        # save the new states to the heap
        heapq.heappush(states, (f, maxH, minH, 1 / iterations[0], currentState, nodes1, nodes2))
        iterations[0] += 1

    def Search(self, grid: Grid, nodes: set[Node], agents: list[Agent], i: int) -> Tuple[list[Node]]:
        """
        Searches for the goal.

        Args:
            grid (Grid): The grid representing the environment.
            nodes (set[Node]): The set of nodes representing the goal.
            agents (list[Agent]): The list of agents.
            i (int): The iteration count.

        Returns:
            Tuple[list[Node]]: The list of actions to reach the goal.
        """
        from heuristics import MultiAgentHeuristic1

        # initialization of the state
        nextGrid: Grid = grid
        nextAgent: MultiAgent = self
        nextNodes: set[Node] = nodes

        # nextNodes1 and nextNodes2 are determined by how the heuristic divides the packages between the agents
        _, _, nextNodes1, nextNodes2 = MultiAgentHeuristic1(nextGrid,
                                             tuple((set(d[0] for d in nextAgent.agent1.GetDropdowns())
                                                    .union({nextAgent.agent1.coordinates}),
                                              set(d[0] for d in nextAgent.agent2.GetDropdowns())
                                              .union({nextAgent.agent2.coordinates}))), nextNodes)

        nextInterference: InterferingAgent = [agent for agent in agents if isinstance(agent, InterferingAgent)][0]
        limit = 0
        states: list[Tuple[int, int, int, MultiAgentState]] = []
        visitedStates: dict[MultiAgentState, int] = {}
        self.cost = i
        iterations = [1]
        listT = []
        maxT = float('-inf')

        # main loop of expanding the states of the a* algorithm
        while nextAgent.score != Grid.numOfPackages:
            st = time.time()

            if limit >= self.l:
                return self.ExceededLimit(nextAgent)
            limit += 1

            # get possible actions for each agent
            actions = nextAgent.GetActions(nextGrid, (nextNodes1, nextNodes2))

            nextAgent.Expand(nextGrid, nextInterference, nextNodes, iterations, actions, states, visitedStates)

            T = round(time.time() - st, ROUND_DIGITS) # pylint: disable=invalid-name
            listT.append(T)
            maxT = max(maxT, T)

            # in case every node was visited and the state didn't change so problem is probably unsolveable
            if not states:
                print("no states left, problem might be unsolveable.")
                self.done = True
                return [], []

            # pop the next state and setup for the next iteration
            f, maxH, minH, _, nextState, nextNodes1, nextNodes2 = heapq.heappop(states)

            if f == float('inf'):
                print("no states left, problem might be unsolveable.")
                self.done = True
                return [], []

            nextGrid: Grid = nextState.grid
            nextAgent: MultiAgent = nextState.agent
            nextInterference: InterferingAgent = nextState.interfering
            nextNodes: set[Node] = nextAgent.FormulateGoal(nextGrid, None)

            assert nextNodes or nextAgent.GetDropdowns() or nextAgent.score == Grid.numOfPackages,\
            "bug! no nodes left and not done"

        # some debug info, indent the print lines below for more info
        print(f"This expand took T={T} seconds, longest expansion took maxT={maxT} seconds")
        print(f"avg T={round(sum(listT) / len(listT), ROUND_DIGITS)} seconds, Total time: {sum(listT)} seconds")
        print(f'popped f: {f}, maxH: {maxH}, minH: {minH}, g: {nextAgent.cost}')
        print(f"path1: {nextAgent.agent1.seq}\npath2: {nextAgent.agent2.seq}")
        print(f"limit: {limit}")
        print(f"pickups: {nextGrid.GetPickups()}")
        print(f"dropdowns1: {nextAgent.agent1.GetDropdowns()}, dropdowns2: {nextAgent.agent2.GetDropdowns()}")
        print(f"future dropdowns: {nextGrid.GetDropdowns()}")
        print(f"score1: {nextAgent.agent1.score}, score2: {nextAgent.agent2.score}")
        print('\n')
        return nextAgent.agent1.seq, nextAgent.agent2.seq

class MultiAgentState:
    """
    Represents the state of a multi-agent system.

    Attributes:
        grid (Grid): The grid representing the environment.
        agent1 (AStarAgent): The first A* agent.
        agent2 (AStarAgent): The second A* agent.
        interfering (InterferingAgent): The interfering agent.
    """

    def __init__(self, grid: Grid, agent: MultiAgent, interfering: InterferingAgent):
        self.grid: Grid = grid
        self.agent: MultiAgent = agent
        self.interfering: InterferingAgent = interfering

    def __hash__(self):
        return hash(self.ToBaseClasses())

    def __eq__(self, other: MultiAgentState):
        return self.ToBaseClasses() == other.ToBaseClasses()

    def ToBaseClasses(self) ->\
        Tuple[Tuple[Node, int], Tuple[Node, Tuple[Node, int]], Tuple[Node ,Tuple[Node, int]], Tuple[Edge]]:
        """
        Converts the current state of the multi-agent to a tuple of base classes.

        Returns:
            Tuple[Tuple[Node, int], Tuple[Node, Tuple[Node, int]], Tuple[Node ,Tuple[Node, int]], Tuple[Edge]]: 
            A tuple containing the coordinates, pickups, dropdowns, and edges of the multi-agent.
        """
        return (self.agent.agent1.coordinates, self.agent.agent1.GetPickups(),
                self.agent.agent1.GetDropdowns(), self.agent.agent2.coordinates,
                self.agent.agent2.GetPickups(), self.agent.agent2.GetDropdowns(),
                tuple(self.grid.fragEdges))
