"""ChromaDB vector store service."""

from typing import List, Optional, Dict, Any


class ChromaService:
    """Service for managing vector store with ChromaDB."""

    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name
        self.documents: Dict[str, Any] = {}

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store."""
        for doc in documents:
            doc_id = doc.get("id")
            if doc_id:
                self.documents[doc_id] = doc

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for documents similar to the query."""
        results = []
        for doc_id, doc in self.documents.items():
            results.append(doc)
        return results[:top_k]

    def delete_documents(self, doc_ids: List[str]) -> None:
        """Delete documents from the vector store."""
        for doc_id in doc_ids:
            if doc_id in self.documents:
                del self.documents[doc_id]

    def get_collection(self):
        """Get the current collection."""
        return self.documents
