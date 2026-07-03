"""Memory agent for managing conversation and context."""

from typing import Dict, Any, List


class MemoryAgent:
    """Agent responsible for managing conversation memory."""

    def __init__(self):
        self.name = "MemoryAgent"
        self.description = "Manages conversation history and context"
        self.memory: List[Dict[str, Any]] = []

    def store(self, interaction: Dict[str, Any]) -> None:
        """Store an interaction in memory."""
        self.memory.append(interaction)

    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context from memory."""
        return self.memory[-5:] if len(self.memory) > 0 else []

    def clear(self) -> None:
        """Clear memory."""
        self.memory = []
