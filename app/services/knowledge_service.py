"""
Knowledge Service.

Uses the LangGraph workflow to answer questions.
"""

from app.graph.workflow import KnowledgeWorkflow
from app.graph.state import KnowledgeState
from app.knowledge.response import KnowledgeResponse
from app.memory.conversation_memory import ConversationMemory


class KnowledgeService:
    """
    Main service for answering knowledge questions.
    """

    def __init__(self):

        self.workflow = (
            KnowledgeWorkflow()
            .compile()
        )

        self.memory = ConversationMemory()

    def ask(
        self,
        question: str,
    ) -> KnowledgeResponse:
        """
        Ask a question using the LangGraph workflow.
        """

        # ----------------------------------
        # Build workflow state
        # ----------------------------------

        state = KnowledgeState(
            original_question=question,
            question=question,
            history=self.memory.context(),
            action="",
            search_results=[],
            context="",
            answer="",
        )

        # ----------------------------------
        # Execute workflow
        # ----------------------------------

        result = self.workflow.invoke(state)

        answer = result["answer"]

        sources = result.get(
            "search_results",
            [],
        )

        # ----------------------------------
        # Save conversation
        # ----------------------------------

        self.memory.add(
            question,
            answer,
        )

        return KnowledgeResponse(
            answer=answer,
            sources=sources,
        )