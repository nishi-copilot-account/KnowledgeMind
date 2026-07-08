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

    ###########################################################
    # RAG Generation
    ###########################################################

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate an answer using retrieved context.
        """

        prompt = f"""
You are KnowledgeMind,
an intelligent personal knowledge assistant.

You MUST answer ONLY from the supplied context.

==================================================
RULES
==================================================

1. NEVER invent or assume information.

2. If the answer exists in the context,
answer confidently.

3. If asked about a person,
include ALL known attributes available.

Example:

Question:
Who is John?

Good Answer:

John is an employee.

Department: IT

Salary: 100

4. If asked about salary,
mention the employee's name.

5. If asked about department,
mention the employee's name.

6. If asked about an employee,
summarize every known attribute instead of replying
with only the person's name.

7. The context may contain Conversation History.

Use it to resolve references such as:

he
she
his
her
they
them
it
this employee
that person

before answering.

8. The context may contain an
Analysis Result.

If it exists:

• Trust it completely.
• Do NOT recompute values.
• Use it as the primary source.

9. If there is no Analysis Result,
reason only from the retrieved knowledge.

10. Never contradict the supplied context.

11. Keep answers concise,
but include all useful information.

12. If the answer is genuinely absent,
reply EXACTLY:

I couldn't find this information in the indexed knowledge.

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

        print("\n" + "=" * 60)
        print("CONTEXT SENT TO LLM")
        print("=" * 60)
        print(context)
        print("=" * 60)

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

    ###########################################################
    # Generic Prompt Generation
    ###########################################################

    def generate_prompt(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from a custom prompt.
        """

        logger.info(
            "Generating custom prompt using Ollama"
        )

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