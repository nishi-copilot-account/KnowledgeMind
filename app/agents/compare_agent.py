"""
Compare Agent.

Compares retrieved knowledge from multiple documents.
"""


class CompareAgent:

    def compare(
        self,
        context: str,
    ) -> str:
        """
        Return a comparison summary.
        """

        if not context.strip():
            return "No information available for comparison."

        sections = context.split("--------------------")

        if len(sections) < 2:
            return (
                "Only one document was found. "
                "Comparison requires multiple documents."
            )

        output = []

        for index, section in enumerate(
            sections,
            start=1,
        ):
            output.append(
                f"Document {index}"
            )
            output.append(
                "----------------"
            )
            output.append(
                section.strip()
            )
            output.append("")

        return "\n".join(output)