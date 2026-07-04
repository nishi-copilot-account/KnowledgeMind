"""
KnowledgeMind AI Assistant
"""

from app.services.knowledge_service import KnowledgeService


def main():

    service = KnowledgeService()

    print("=" * 60)
    print("        KnowledgeMind AI")
    print("=" * 60)

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        print("\nThinking...\n")

        answer = service.ask(question)

        print(answer)

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()