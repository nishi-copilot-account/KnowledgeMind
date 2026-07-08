"""
Semantic retriever.
"""

from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore


class KnowledgeRetriever:
    """
    Retrieves relevant knowledge from ChromaDB.
    """

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        source_document: str | None = None,
    ):
        """
        Retrieve the most relevant chunks.

        If source_document is supplied, search only
        within that document.
        """

        embedding = self.embedding_service.embed(
            question
        )

        return self.vector_store.search(
            embedding=embedding,
            top_k=top_k,
            source_document=source_document,
        )