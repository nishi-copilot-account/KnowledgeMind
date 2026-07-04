from app.retrieval.retriever import KnowledgeRetriever


def main():

    retriever = KnowledgeRetriever()

    question = "What is OCR?"

    results = retriever.retrieve(question)

    print("=" * 60)
    print("Semantic Search Results")
    print("=" * 60)

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")

        print(f"Distance : {result.score:.4f}")

        print(f"Source : {result.chunk.source_document}")

        print(f"Page   : {result.chunk.page_number}")

        print()

        print(result.chunk.text[:250])

        print("-" * 60)


if __name__ == "__main__":
    main()