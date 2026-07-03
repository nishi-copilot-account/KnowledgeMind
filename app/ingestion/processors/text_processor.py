"""
Text processing for KnowledgeMind.

Responsible for cleaning and normalizing extracted text.
"""


class TextProcessor:

    def process(self, text: str) -> str:
        """
        Clean extracted text.
        """

        if not text:
            return ""

        # Remove leading/trailing whitespace
        text = text.strip()

        # Split into lines
        lines = text.splitlines()

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if line:
                cleaned_lines.append(line)

        # Join with newline
        cleaned_text = "\n".join(cleaned_lines)

        return cleaned_text