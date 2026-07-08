"""
Reasoning Agent.

Prepares retrieved knowledge before sending it to the LLM.
"""

import re

from app.knowledge.search_result import KnowledgeSearchResult


class ReasoningAgent:
    """
    Cleans, structures and optimizes retrieved knowledge.
    """

    def prepare_context(
        self,
        results: list[KnowledgeSearchResult],
        question: str,
        history: str = "",
        action: str = "retrieve",
    ) -> str:

        if not results:
            return ""

        sections = []
        seen = set()

        for result in results:

            text = result.chunk.text.strip()
            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r"[ \t]+", " ", text)

            normalized = text.lower().strip()

            if normalized in seen:
                continue

            seen.add(normalized)

            seen.add(text)

            text = self._format_tables(text)

            section = (
                "==================================================\n"
                f"Document: {result.chunk.source_document}\n"
                f"Page: {result.chunk.page_number}\n\n"
                "==================================================\n\n"
                f"{text}"
            )

            sections.append(section)

        context = "\n\n".join(sections)

        ###########################################################
        # Agentic reasoning
        ###########################################################

        if action == "compare":

            context = self._prepare_compare_context(
                context,
            )

        elif self._is_count_question(question):

            context = self._prepare_count_context(
                context,
            )

        elif self._is_filter_question(question):

            context = self._prepare_filter_context(
                context,
                question,
            )

        elif self._is_max_question(question):

            context = self._prepare_max_context(
                context,
            )

        elif self._is_min_question(question):

            context = self._prepare_min_context(
                context,
            )

        elif self._is_average_question(question):

            context = self._prepare_average_context(
                context,
            )

        elif self._is_group_question(question):

            context = self._prepare_group_context(
                context,
            )

        elif self._is_sort_question(question):

            context = self._prepare_sort_context(
                context,
            )

        ###########################################################
        # Conversation History
        ###########################################################

        if history:

            context = (
            "==============================\n"
            "REQUEST\n"
            "==============================\n"
            f"{question}\n\n"
            "==============================\n"
            "RETRIEVED KNOWLEDGE\n"
            "==============================\n"
            f"Relevant Chunks: {len(results)}\n\n"
            + context
        )

        return context

    ###########################################################
    # Question classifiers
    ###########################################################

    def _is_count_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "how many",
            "count",
            "number of",
            "total",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_filter_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "show",
            "list",
            "only",
            "employees",
            "department",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_max_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "highest",
            "maximum",
            "max",
            "largest",
            "most",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_min_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "lowest",
            "minimum",
            "least",
            "smallest",
            "min",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_average_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "average",
            "mean",
            "avg",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_group_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "group",
            "group by",
            "categorize",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    def _is_sort_question(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        keywords = [
            "sort",
            "order",
            "ascending",
            "descending",
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    ###########################################################
    # Compare
    ###########################################################

    def _prepare_compare_context(
        self,
        context: str,
    ) -> str:

        return (
            "Comparison Context\n"
            "====================\n\n"
            + context
        )

    ###########################################################
    # Count
    ###########################################################

    def _prepare_count_context(
        self,
        context: str,
    ) -> str:

        employees = context.count(
            "Employee Record"
        )

        return (
            context
            + "\n\n"
            + f"Detected Employees: {employees}"
        )

    ###########################################################
    # Filter
    ###########################################################

    def _prepare_filter_context(
        self,
        context: str,
        question: str,
    ) -> str:

        words = [
            word
            for word in question.lower().split()
            if len(word) > 2
        ]

        filtered = []

        for line in context.splitlines():

            lower = line.lower()

            if any(
                word in lower
                for word in words
            ):
                filtered.append(line)

        if not filtered:
            return context

        return (
            context
            + "\n\nRelevant Lines\n"
            "----------------\n"
            + "\n".join(filtered)
        )

    ###########################################################
    # Maximum
    ###########################################################

    def _prepare_max_context(
        self,
        context: str,
    ) -> str:

        return (
            "Maximum Analysis\n"
            "================\n\n"
            + context
        )

    ###########################################################
    # Minimum
    ###########################################################

    def _prepare_min_context(
        self,
        context: str,
    ) -> str:

        return (
            "Minimum Analysis\n"
            "================\n\n"
            + context
        )

    ###########################################################
    # Average
    ###########################################################

    def _prepare_average_context(
        self,
        context: str,
    ) -> str:

        return (
            "Average Analysis\n"
            "================\n\n"
            + context
        )

    ###########################################################
    # Group
    ###########################################################

    def _prepare_group_context(
        self,
        context: str,
    ) -> str:

        return (
            "Group Analysis\n"
            "==============\n\n"
            + context
        )

    ###########################################################
    # Sort
    ###########################################################

    def _prepare_sort_context(
        self,
        context: str,
    ) -> str:

        return (
            "Sorted Analysis\n"
            "===============\n\n"
            + context
        )

    ###########################################################
    # Table Formatter
    ###########################################################

    def _format_tables(
        self,
        text: str,
    ) -> str:
        """
        Convert OCR table into structured employee records.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if len(lines) < 6:
            return text

        if lines[0].lower() != "name department salary":
            return text

        rows = lines[1:]

        if len(rows) % 3 != 0:
            return text

        output = []

        for i in range(
            0,
            len(rows),
            3,
        ):

            output.append(
                "Employee Record"
            )

            output.append(
                "---------------"
            )

            output.append(
                f"Name: {rows[i]}"
            )

            output.append(
                f"Department: {rows[i + 1]}"
            )

            output.append(
                f"Salary: {rows[i + 2]}"
            )

            output.append("")

        return "\n".join(output)