from app.ingestion.pipeline import KnowledgePipeline
from app.knowledge.normalizer import KnowledgeNormalizer


def main():

    pipeline = KnowledgePipeline()

    document = pipeline.process(
        "data/documents/test_club.pdf"
    )

    normalizer = KnowledgeNormalizer()

    chunks = normalizer.normalize(document)

    print("=" * 60)
    print(f"Chunks Created : {len(chunks)}")
    print("=" * 60)

    for chunk in chunks:

        print(f"Chunk ID : {chunk.chunk_id}")
        print(f"Document : {chunk.source_document}")
        print(f"Type     : {chunk.source_type}")
        print(f"Page     : {chunk.page_number}")
        print()

        print(chunk.text[:200])

        print()

        print(f"Images : {len(chunk.images)}")
        print(f"Tables : {len(chunk.tables)}")

        print("-" * 60)


if __name__ == "__main__":
    main()