"""
Indexes documents into the KnowledgeMind vector database.
"""

from app.chunking.chunk_builder import ChunkBuilder
from app.ingestion.pipeline import KnowledgePipeline
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore


class IndexingService:

    def __init__(self):

        self.pipeline = KnowledgePipeline()
        self.chunk_builder = ChunkBuilder()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def index_document(
        self,
        file_path: str,
    ):

        print("\nProcessing document...")

        knowledge = self.pipeline.process(file_path)

        # ---------------------------------------
        # Skip duplicate documents
        # ---------------------------------------

        if self.vector_store.document_exists(
            knowledge.filename,
        ):

            print("\nDocument already indexed.")
            print("Skipping duplicate indexing.")

            return

        chunks = self.chunk_builder.build(
            knowledge
        )

        for chunk in chunks:

            embedding = self.embedding_service.embed(
                chunk.text
            )

            self.vector_store.add(
                chunk,
                embedding,
            )

        print(f"\nIndexed {len(chunks)} chunks successfully.")