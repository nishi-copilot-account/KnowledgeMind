"""
LLM service for KnowledgeMind.
"""

import os

from openai import OpenAI


class LLMService:
    """
    Wrapper around an LLM provider.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate an answer using retrieved context.
        """

        prompt = f"""
You are KnowledgeMind.

Answer ONLY using the provided context.

If the answer is not present, say:

"I couldn't find this information in the indexed knowledge."

Context:

{context}

Question:

{question}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content