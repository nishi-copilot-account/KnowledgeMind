"""Retriever component for querying the knowledge base."""

from typing import List, Dict, Any


class Retriever:
    """Retrieves relevant documents from the knowledge base."""

    def __init__(self, vector_store=None):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents relevant to the query."""
        if self.vector_store:
            return self.vector_store.search(query, top_k=top_k)
        return []

    def retrieve_with_scores(self, query: str, top_k: int = 5) -> List[tuple]:
        """Retrieve documents with relevance scores."""
        results = self.retrieve(query, top_k)
        return [(doc, 0.95) for doc in results]
