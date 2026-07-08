"""
Compare Agent.

Compares retrieved knowledge from multiple documents.
"""
from app.llm.llm_service import LLMService


class CompareAgent:

    def __init__(self):
        self.llm = LLMService()

    def compare(self, context: str) -> str:
        """
        Compare multiple documents using the LLM.
        """

        if not context.strip():
            return "No information available for comparison."

        prompt = f"""
    You are KnowledgeMind.

    You are an expert document comparison assistant.

    The following knowledge was retrieved from multiple documents.

    Compare the documents and produce a professional comparison.

    Instructions:

    - Use Markdown headings.
    - Clearly identify similarities.
    - Clearly identify differences.
    - Highlight unique information in each document.
    - If tables are present, compare them naturally.
    - Do not invent information.
    - End with a short conclusion.

    ========================================

    {context}

    ========================================

    Comparison:
    """

        return self.llm.generate_prompt(prompt)