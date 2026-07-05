from app.agents.planner_agent import PlannerAgent


def main():

    planner = PlannerAgent()

    while True:

        question = input("\nQuestion: ")

        if question == "exit":
            break

        action = planner.plan(question)

        print("\nPlanner chose:", action)


if __name__ == "__main__":
    main()