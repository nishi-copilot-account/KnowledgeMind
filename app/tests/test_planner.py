from app.agents.planner_agent import PlannerAgent


def main():

    planner = PlannerAgent()

    questions = [

        "What is John's salary?",

        "Summarize this document",

        "Compare John and Alice",

        "Difference between HR and IT",

    ]

    for question in questions:

        action = planner.execute(question)

        print(f"{question}")

        print(f"Action : {action}")

        print("-" * 50)


if __name__ == "__main__":
    main()