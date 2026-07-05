from app.services.indexing_service import IndexingService
from app.services.knowledge_service import KnowledgeService
from app.services.statistics_service import StatisticsService


def main():

    indexing_service = IndexingService()
    knowledge_service = KnowledgeService()
    statistics_service = StatisticsService()

    while True:

        print("\n" + "=" * 60)
        print("KnowledgeMind AI")
        print("=" * 60)

        print("1. Index Document")
        print("2. Chat with Knowledge")
        print("3. Collection Statistics")
        print("4. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            path = input("\nDocument Path: ")

            indexing_service.index_document(path)

        elif choice == "2":

            print("\n" + "=" * 60)
            print("KnowledgeMind Chat")
            print("Type 'exit' to return to the main menu.")
            print("=" * 60)

            while True:

                question = input("\nYou > ").strip()

                if question.lower() in {
                    "exit",
                    "quit",
                    "back",
                }:
                    break

                if not question:
                    continue

                response = knowledge_service.ask(question)

                print("\nKnowledgeMind >\n")
                print(response.answer)

                if response.sources:

                    print("\n" + "-" * 60)
                    print("Sources")
                    print("-" * 60)

                    shown = set()

                    for result in response.sources:

                        key = (
                            result.chunk.source_document,
                            result.chunk.page_number,
                        )

                        if key in shown:
                            continue

                        shown.add(key)

                        print(
                            f"• {result.chunk.source_document} "
                            f"(Page {result.chunk.page_number})"
                        )

        elif choice == "3":

            statistics = statistics_service.statistics()

            print("\n" + "=" * 60)
            print("Collection Statistics")
            print("=" * 60)

            print(
                f"Documents : {statistics['document_count']}"
            )
            print(
                f"Chunks    : {statistics['chunk_count']}"
            )

            print("\nIndexed Documents")

            for document in statistics["documents"]:

                print(f"• {document}")

        elif choice == "4":

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid choice.")


if __name__ == "__main__":
    main()