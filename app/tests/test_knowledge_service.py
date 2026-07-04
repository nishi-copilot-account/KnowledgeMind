from app.services.knowledge_service import KnowledgeService


def main():

    service = KnowledgeService()

    print("=" * 60)
    print("KnowledgeMind")
    print("=" * 60)

    question = input("\nAsk a question: ")

    answer = service.ask(question)

    print("\nAnswer\n")

    print(answer)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()