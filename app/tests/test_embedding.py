from app.retrieval.embedding_service import EmbeddingService


def main():

    service = EmbeddingService()

    text = (
        "KnowledgeMind is an Agentic AI Personal Knowledge System."
    )

    vector = service.embed(text)

    print("=" * 60)
    print("Embedding Generated")
    print("=" * 60)

    print(f"Dimensions : {len(vector)}")

    print("\nFirst 10 values:")

    print(vector[:10])


if __name__ == "__main__":
    main()