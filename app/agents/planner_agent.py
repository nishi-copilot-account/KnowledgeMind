"""
Planner Agent.

Decides how a user question should be processed.
"""

from app.agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):

    def execute(
        self,
        question: str,
    ) -> str:
        """
        Decide which workflow should answer the question.
        """

        question = question.lower()

        if any(
            word in question
            for word in [
                "summarize",
                "summary",
            ]
        ):
            return "summarize"

        if any(
            word in question
            for word in [
                "compare",
                "difference",
            ]
        ):
            return "reason"

        return "retrieve"