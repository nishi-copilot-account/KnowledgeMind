"""
Collection statistics service.
"""

from app.retrieval.vector_store import VectorStore


class StatisticsService:

    def __init__(self):

        self.vector_store = VectorStore()

    def show(self):

        stats = self.vector_store.statistics()

        print("\n" + "=" * 60)
        print("Knowledge Collection")
        print("=" * 60)

        print(f"\nDocuments Indexed : {stats['document_count']}")
        print(f"Chunks Stored     : {stats['chunk_count']}")
        print("Embedding Model   : sentence-transformers/all-MiniLM-L6-v2")
        print("LLM Model         : llama3.2:3b")

        print("\nIndexed Documents\n")

        if not stats["documents"]:
            print("No documents indexed.")
            return

        for document in stats["documents"]:
            print(f"• {document}")