from app.graph.workflow import KnowledgeWorkflow


def main():

    workflow = KnowledgeWorkflow().compile()

    result = workflow.invoke(
        {
            "question": "What is John's salary?",
            "search_results": [],
            "context": "",
            "answer": "",
        }
    )

    print("\nAnswer")
    print("=" * 60)

    print(result["answer"])


if __name__ == "__main__":
    main()