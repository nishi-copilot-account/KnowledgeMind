"""Response agent for generating final responses."""

from typing import Dict, Any


class ResponseAgent:
    """Agent responsible for generating final responses."""

    def __init__(self):
        self.name = "ResponseAgent"
        self.description = "Generates final responses"

    def generate_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate a response based on query and context."""
        return f"Response to: {query}"

    def format_response(self, response: str) -> Dict[str, Any]:
        """Format the response for presentation."""
        return {
            "agent": self.name,
            "response": response,
            "formatted": True,
            "includes_citations": True
        }
