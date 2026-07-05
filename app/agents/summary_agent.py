class SummaryAgent:

    def summarize(
        self,
        context: str,
    ) -> str:

        if not context:
            return "No information available."

        lines = context.splitlines()

        return "\n".join(lines[:15])