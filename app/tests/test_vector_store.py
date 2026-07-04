from app.ingestion.pipeline import KnowledgePipeline
from app.knowledge.normalizer import KnowledgeNormalizer
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore


def main():

    pipeline = KnowledgePipeline()

    document = pipeline.process(
        "data/documents/test_club.pdf"
    )

    normalizer = KnowledgeNormalizer()

    chunks = normalizer.normalize(document)

    embedding_service = EmbeddingService()

    vector_store = VectorStore()

    for chunk in chunks:

        embedding = embedding_service.embed(
            chunk.text
        )

        vector_store.add(
            chunk,
            embedding,
        )

        print(
            f"Stored chunk {chunk.chunk_id}"
        )

    print("\nCompleted.")


if __name__ == "__main__":
    main()