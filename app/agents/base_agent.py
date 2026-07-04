"""
Base class for all KnowledgeMind agents.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base interface for every agent.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the agent.
        """
        raise NotImplementedError