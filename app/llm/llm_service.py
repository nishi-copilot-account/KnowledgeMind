"""
LLM service using Ollama.
"""

import ollama

from app.utils.logger import logger


class LLMService:
    """
    Wrapper around Ollama.
    """

    def __init__(self):

        self.model = "llama3.2:3b"

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

Answer ONLY using the context below.

If the answer cannot be found, say:

"I couldn't find this information in the indexed knowledge."

Context:

{context}

Question:

{question}
"""

        logger.info("Generating response using Ollama")

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]