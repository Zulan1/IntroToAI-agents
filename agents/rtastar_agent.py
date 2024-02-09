from __future__ import annotations
from agents.astar_agent import AStarAgent
from type_aliases import Node

class RTAStarAgent(AStarAgent):
    """class for Greedy Agent"""
    l: int = 10

    def ExceededLimit(self, nextAgent: RTAStarAgent) -> list[Node]:
        """Handler for when the agent exceeded the limit"""
        return [nextAgent.seq[0]]
