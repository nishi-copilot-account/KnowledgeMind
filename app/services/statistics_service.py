"""
Collection statistics service.
"""

from app.retrieval.vector_store import VectorStore


class StatisticsService:
    """
    Provides collection statistics for both
    the console application and Streamlit UI.
    """

    def __init__(self):

        self.vector_store = VectorStore()

    def statistics(self) -> dict:
        """
        Return collection statistics.
        """

        return self.vector_store.statistics()

    def show(self):
        """
        Print statistics to the console.
        """

        stats = self.statistics()

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