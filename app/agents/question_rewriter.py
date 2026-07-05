"""
Question Rewriter.

Converts follow-up questions into standalone questions.
Uses simple rules first and falls back to the LLM only when necessary.
"""

import re

import ollama

from app.utils.logger import logger


class QuestionRewriter:

    def __init__(self):

        self.model = "llama3.2:3b"

    ###########################################################
    # Public API
    ###########################################################

    def rewrite(
        self,
        question: str,
        history: str,
    ) -> str:
        """
        Rewrite follow-up questions into standalone questions.
        """

        question = question.strip()

        #
        # No history
        #

        if not history:

            return question

        #
        # Already standalone?
        #

        if self._is_standalone(question):

            logger.info(
                "Question already standalone."
            )

            return question

        #
        # Common follow-up?
        #

        rewritten = self._rule_based_rewrite(
            question,
            history,
        )

        if rewritten:

            logger.info(
                "Rule-based rewrite: %s",
                rewritten,
            )

            return rewritten

        #
        # LLM rewrite
        #

        return self._llm_rewrite(
            question,
            history,
        )

    ###########################################################
    # Standalone detection
    ###########################################################

    def _is_standalone(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        standalone_patterns = [

            "who is",
            "what is",
            "where is",
            "when is",
            "why is",

            "how many",

            "list",

            "show",

            "compare",

            "summarize",

            "salary",

            "department",

            "employee",

            "employees",
        ]

        return any(
            pattern in question
            for pattern in standalone_patterns
        )

    ###########################################################
    # Rule-based rewriting
    ###########################################################

    def _rule_based_rewrite(
        self,
        question: str,
        history: str,
    ) -> str | None:

        question_lower = question.lower()

        #
        # Extract latest employee name from history
        #

        latest_name = self._extract_latest_name(
            history,
        )

        #
        # Which department?
        #

        if (
            "which department"
            in question_lower
            and latest_name
        ):

            return (
                f"Which department does "
                f"{latest_name} work in?"
            )

        #
        # What about Alice?
        #

        if question_lower.startswith(
            "what about "
        ):

            name = question[11:].strip()

            if name:

                return f"Who is {name}?"

        #
        # And Alice?
        #

        if question_lower.startswith(
            "and "
        ):

            name = question[4:].strip()

            if name:

                return f"Who is {name}?"

        #
        # Who earns more?
        #

        if (
            "who earns more"
            in question_lower
        ):

            return (
                "Compare the salaries "
                "of all employees."
            )

        #
        # Which one?
        #

        if (
            question_lower
            == "which one?"
        ):

            return (
                "Which employee "
                "are you referring to?"
            )

        return None

    ###########################################################
    # LLM rewrite
    ###########################################################

    def _llm_rewrite(
        self,
        question: str,
        history: str,
    ) -> str:

        logger.info(
            "Rewriting follow-up using LLM..."
        )

        prompt = f"""
Conversation:

{history}

Rewrite the user's last question so it
becomes completely standalone.

Do NOT answer it.

Return ONLY the rewritten question.

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

        rewritten = (
            response["message"]["content"]
            .strip()
        )

        logger.info(
            "LLM Rewrite: %s",
            rewritten,
        )

        return rewritten

    ###########################################################
    # Utilities
    ###########################################################

    def _extract_latest_name(
        self,
        history: str,
    ) -> str | None:
        """
        Find the last capitalized name
        appearing in the conversation.
        """

        matches = re.findall(
            r"\b[A-Z][a-z]+\b",
            history,
        )

        ignore = {

            "User",

            "Assistant",

            "KnowledgeMind",

            "Document",

            "Page",

            "Department",

            "Salary",

            "Employee",

            "Record",
        }

        names = [

            name

            for name in matches

            if name not in ignore
        ]

        if names:

            return names[-1]

        return None