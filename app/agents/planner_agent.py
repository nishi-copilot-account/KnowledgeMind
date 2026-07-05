"""
Planner Agent.

Decides which workflow action should execute.
Uses rule-based routing first and falls back to the LLM.
"""

import ollama

from app.utils.logger import logger


class PlannerAgent:

    def __init__(self):

        self.model = "llama3.2:3b"

    ###########################################################
    # Public API
    ###########################################################

    def plan(
        self,
        question: str,
        has_history: bool = False,
    ) -> str:
        """
        Decide which workflow should execute.
        """

        question_lower = question.lower()

        if self._is_followup(
            question_lower,
            has_history,
        ):
            return "retrieve"

        if self._is_chat(question_lower):
            return "chat"

        if self._is_summary(question_lower):
            return "summarize"

        if self._is_compare(question_lower):
            return "compare"

        if self._is_retrieve(question_lower):
            return "retrieve"

        return self._llm_plan(question)

    ###########################################################
    # Chat
    ###########################################################

    def _is_chat(
        self,
        question: str,
    ) -> bool:

        words = question.split()

        return (
            "hello" in words
            or "hi" in words
            or "hey" in words
            or question.startswith("good morning")
            or question.startswith("good evening")
            or "how are you" in question
        )

    ###########################################################
    # Summary
    ###########################################################

    def _is_summary(
        self,
        question: str,
    ) -> bool:

        keywords = [

            "summarize",

            "summary",

            "overview",

            "brief",

            "short summary",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    ###########################################################
    # Compare
    ###########################################################

    def _is_compare(
        self,
        question: str,
    ) -> bool:

        keywords = [

            "compare",

            "difference",

            "versus",

            "vs",

            "higher",

            "lower",

            "more than",

            "less than",

            "earns more",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    ###########################################################
    # Retrieval
    ###########################################################

    def _is_retrieve(
        self,
        question: str,
    ) -> bool:

        keywords = [

            "who is",

            "what is",

            "where is",

            "salary",

            "department",

            "employee",

            "employees",

            "works",

            "working",

            "manager",

            "designation",

            "project",

            "phone",

            "email",

            "location",

            "address",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    ###########################################################
    # Follow-up
    ###########################################################

    def _is_followup(
        self,
        question: str,
        has_history: bool,
    ) -> bool:

        if not has_history:
            return False

        words = question.split()

        if not words:
            return False

        followups = {

            "which",

            "what",

            "who",

            "where",

            "when",

            "why",

            "how",

            "also",

            "then",

            "their",

            "his",

            "her",

            "it",

            "they",
        }

        if words[0] in followups:

            logger.info(
                "Planner (memory): retrieve"
            )

            return True

        return False

    ###########################################################
    # LLM
    ###########################################################

    def _llm_plan(
        self,
        question: str,
    ) -> str:

        logger.info(
            "Planner using LLM..."
        )

        prompt = f"""
You are the planning agent for KnowledgeMind.

Choose exactly ONE action.

retrieve
summarize
compare
chat

Reply with ONLY one word.

Question:

{question}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        action = (
            response["message"]["content"]
            .strip()
            .lower()
        )

        if action not in {

            "retrieve",

            "summarize",

            "compare",

            "chat",
        }:

            action = "retrieve"

        logger.info(
            "Planner chose: %s",
            action,
        )

        return action