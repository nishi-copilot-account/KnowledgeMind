"""
Conversation memory for KnowledgeMind.
"""


class ConversationMemory:
    """
    Stores recent conversation history.
    """

    def __init__(self):

        self.history = []

    def add(
        self,
        question: str,
        answer: str,
    ):

        self.history.append(
            {
                "question": question,
                "answer": answer,
            }
        )

        # Keep only last 5 interactions
        self.history = self.history[-5:]

    def context(self) -> str:

        if not self.history:
            return ""

        lines = []

        for item in self.history:

            lines.append(f"User: {item['question']}")
            lines.append(f"Assistant: {item['answer']}")

        return "\n".join(lines)

    def clear(self):

        self.history.clear()