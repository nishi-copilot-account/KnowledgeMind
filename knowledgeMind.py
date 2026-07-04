from app.services.indexing_service import IndexingService
from app.services.knowledge_service import KnowledgeService


def main():

    indexing_service = IndexingService()
    knowledge_service = KnowledgeService()

    while True:

        print("\n" + "=" * 60)
        print("KnowledgeMind AI")
        print("=" * 60)

        print("1. Index Document")
        print("2. Ask Question")
        print("3. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            path = input("\nDocument Path: ")

            indexing_service.index_document(path)

        elif choice == "2":

            question = input("\nQuestion: ")

            response = knowledge_service.ask(question)

            print("\nAnswer\n")

            print(response.answer)

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

            print("\nGoodbye!")

            break

        else:

            print("\nInvalid choice.")


if __name__ == "__main__":
    main()