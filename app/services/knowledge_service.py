"""
Knowledge service.

Coordinates retrieval and LLM generation.
"""

from app.llm.llm_service import LLMService
from app.retrieval.retriever import KnowledgeRetriever


class KnowledgeService:
    """
    Main service for answering knowledge questions.
    """

    def __init__(self):

        self.retriever = KnowledgeRetriever()

        self.llm = LLMService()

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:
        """
        Ask a question about the indexed knowledge.
        """

        results = self.retriever.retrieve(
            question,
            top_k,
        )

        context = "\n\n".join(
            result.chunk.text
            for result in results
        )

        return self.llm.generate(
            question=question,
            context=context,
        )