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

4. Reply
"I couldn't find this information in the indexed knowledge."
ONLY if the answer is genuinely absent.

5. If the context contains tables, use the table values.

6. Never ignore information present in the context.

7. The context may contain previous conversation history.
Use it to resolve references such as:
he, she, they, it, this, that, his, her, etc.

8. If the context contains an
"Analysis Result"
section, ALWAYS trust that analysis.

9. Do NOT recompute values that already appear inside
"Analysis Result".

10. Use the Analysis Result as the primary source,
then explain it naturally.

11. If Analysis Result is absent,
reason using the retrieved knowledge.

==================================================
CONVERSATION AND KNOWLEDGE CONTEXT
==================================================

{context}

==================================================
QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""

        logger.info(
            "Generating response using Ollama"
        )

        # --------------------------------------------------
        # Debug
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("CONTEXT SENT TO LLM")
        print("=" * 60)
        print(context)
        print("=" * 60)

        # --------------------------------------------------

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