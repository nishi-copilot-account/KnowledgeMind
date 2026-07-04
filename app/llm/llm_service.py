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
You are KnowledgeMind, an intelligent personal knowledge assistant.

You must answer ONLY from the supplied context.

Rules:
1. If the answer exists in the context, answer it directly.
2. Be concise and factual.
3. Do NOT invent information.
4. Only reply "I couldn't find this information in the indexed knowledge."
   if the answer is genuinely absent.
5. If the context contains tables, use the table values to answer.
6. Never ignore information present in the context.

======================
CONTEXT
======================

{context}

======================
QUESTION
======================

{question}

======================
ANSWER
======================
"""

        logger.info("Generating response using Ollama")

        # ---------- Debug ----------
        print("\n" + "=" * 60)
        print("CONTEXT SENT TO LLM")
        print("=" * 60)
        print(context)
        print("=" * 60)
        # ---------------------------

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