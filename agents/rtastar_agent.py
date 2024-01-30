from __future__ import annotations
from typing import Tuple
from agents.search_agent import SearchAgent
from agents.astar_agent import AStarAgent
from grid import Grid
from type_aliases import Node

State = Tuple[Grid, SearchAgent]

class RTAStarAgent(AStarAgent):
    """class for Greedy Agent"""
    l: int = 10
    limit: int = 0

    def ExceededLimit(self, nextAgent: RTAStarAgent) -> list[Node]:
        """Handler for when the agent exceeded the limit"""
        self.limit = 0
        return [nextAgent.seq[0]]
