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
    ):

        embedding = self.embedding_service.embed(question)

        results = self.vector_store.search(
            embedding,
            top_k,
        )

        print("\n" + "=" * 60)
        print("RETRIEVED CHUNKS")
        print("=" * 60)

        for index, result in enumerate(results, start=1):

            print(f"\nChunk {index}")
            print("-" * 40)

            print(result.chunk.text)

            print("-" * 40)

            print(f"Score : {result.score:.4f}")

        return results