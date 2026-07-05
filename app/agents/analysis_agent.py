"""
Analysis Agent.

Performs deterministic analysis over structured context before
sending it to the LLM.
"""

import re
from collections import defaultdict


class AnalysisAgent:
    """
    Performs deterministic analysis over structured employee data.
    """

    def analyze(
        self,
        context: str,
        question: str,
    ) -> str:

        question = question.lower()

        employees = self._extract_employees(
            context,
        )

        if not employees:
            return context

        if self._is_max(question):
            return self._highest_salary(
                context,
                employees,
            )

        if self._is_min(question):
            return self._lowest_salary(
                context,
                employees,
            )

        if self._is_average(question):
            return self._average_salary(
                context,
                employees,
            )

        if self._is_count(question):
            return self._count(
                context,
                employees,
            )

        if self._is_sort(question):
            return self._sort(
                context,
                employees,
                question,
            )

        if self._is_group(question):
            return self._group(
                context,
                employees,
            )

        if self._is_filter(question):
            return self._filter(
                context,
                employees,
                question,
            )

        return context

    ###########################################################
    # Question Classifiers
    ###########################################################

    def _is_max(
        self,
        question: str,
    ) -> bool:

        return any(
            word in question
            for word in [
                "highest",
                "maximum",
                "max",
                "most",
            ]
        )

    def _is_min(
        self,
        question: str,
    ) -> bool:

        return any(
            word in question
            for word in [
                "lowest",
                "minimum",
                "least",
                "min",
            ]
        )

    def _is_average(
        self,
        question: str,
    ) -> bool:

        return any(
            word in question
            for word in [
                "average",
                "avg",
                "mean",
            ]
        )

    def _is_count(
        self,
        question: str,
    ) -> bool:

        return any(
            word in question
            for word in [
                "count",
                "how many",
                "number of",
                "total",
            ]
        )

    def _is_sort(
        self,
        question: str,
    ) -> bool:

        return any(
            word in question
            for word in [
                "sort",
                "order",
                "ascending",
                "descending",
            ]
        )

    def _is_group(
        self,
        question: str,
    ) -> bool:

        return "group" in question

    def _is_filter(
        self,
        question: str,
    ) -> bool:

        return (
            "only" in question
            or "show" in question
            or "list" in question
        )

    ###########################################################
    # Highest Salary
    ###########################################################

    def _highest_salary(
        self,
        context: str,
        employees: list[dict],
    ) -> str:

        employee = max(
            employees,
            key=lambda e: e["salary"],
        )

        return (
            context
            + "\n\nAnalysis Result\n"
            + "===============\n"
            + f"Highest Salary: "
            + f"{employee['name']} "
            + f"({employee['salary']:.2f})"
        )

    ###########################################################
    # Lowest Salary
    ###########################################################

    def _lowest_salary(
        self,
        context: str,
        employees: list[dict],
    ) -> str:

        employee = min(
            employees,
            key=lambda e: e["salary"],
        )

        return (
            context
            + "\n\nAnalysis Result\n"
            + "===============\n"
            + f"Lowest Salary: "
            + f"{employee['name']} "
            + f"({employee['salary']:.2f})"
        )

    ###########################################################
    # Average Salary
    ###########################################################

    def _average_salary(
        self,
        context: str,
        employees: list[dict],
    ) -> str:

        average = (
            sum(
                employee["salary"]
                for employee in employees
            )
            / len(employees)
        )

        return (
            context
            + "\n\nAnalysis Result\n"
            + "===============\n"
            + f"Average Salary: {average:.2f}"
        )

    ###########################################################
    # Count
    ###########################################################

    def _count(
        self,
        context: str,
        employees: list[dict],
    ) -> str:

        return (
            context
            + "\n\nAnalysis Result\n"
            + "===============\n"
            + f"Employee Count: {len(employees)}"
        )

    ###########################################################
    # Sort
    ###########################################################

    def _sort(
        self,
        context: str,
        employees: list[dict],
        question: str,
    ) -> str:

        reverse = (
            "descending" in question
        )

        ordered = sorted(
            employees,
            key=lambda e: e["salary"],
            reverse=reverse,
        )

        output = [
            context,
            "",
            "Analysis Result",
            "===============",
            "Employees Sorted by Salary",
            "",
        ]

        for employee in ordered:

            output.append(
                f"{employee['name']} - "
                f"{employee['department']} - "
                f"{employee['salary']:.2f}"
            )

        return "\n".join(output)

    ###########################################################
    # Group
    ###########################################################

    def _group(
        self,
        context: str,
        employees: list[dict],
    ) -> str:

        departments = defaultdict(list)

        for employee in employees:

            departments[
                employee["department"]
            ].append(employee["name"])

        output = [
            context,
            "",
            "Analysis Result",
            "===============",
            "Employees Grouped by Department",
            "",
        ]

        for department in sorted(
            departments
        ):

            output.append(
                f"{department}:"
            )

            for employee in departments[
                department
            ]:

                output.append(
                    f"  • {employee}"
                )

            output.append("")

        return "\n".join(output)

    ###########################################################
    # Filter
    ###########################################################

    def _filter(
        self,
        context: str,
        employees: list[dict],
        question: str,
    ) -> str:

        question = question.lower()

        filtered = []

        for employee in employees:

            if (
                employee["department"].lower()
                in question
            ):

                filtered.append(
                    employee
                )

        if not filtered:
            return context

        output = [
            context,
            "",
            "Analysis Result",
            "===============",
            "Filtered Employees",
            "",
        ]

        for employee in filtered:

            output.append(
                f"{employee['name']} - "
                f"{employee['department']} - "
                f"{employee['salary']:.2f}"
            )

        return "\n".join(output)

    ###########################################################
    # Employee Parser
    ###########################################################

    def _extract_employees(
        self,
        context: str,
    ) -> list[dict]:

        pattern = re.compile(
            r"Name:\s*(.*?)\n"
            r"Department:\s*(.*?)\n"
            r"Salary:\s*([0-9]+(?:\.[0-9]+)?)",
            re.MULTILINE,
        )

        employees = []

        for match in pattern.findall(context):

            employees.append(
                {
                    "name": match[0].strip(),
                    "department": match[1].strip(),
                    "salary": float(match[2]),
                }
            )

        return employees