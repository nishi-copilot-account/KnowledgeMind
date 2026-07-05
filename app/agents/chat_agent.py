"""
Chat Agent.

Handles casual conversation without retrieval.
"""


class ChatAgent:
    """
    Handles greetings and casual conversation.
    """

    def reply(
        self,
        question: str,
    ) -> str:

        question = question.lower()

        if "hello" in question:
            return "Hello! How can I help you today?"

        if "hi" in question:
            return "Hi! What would you like to know?"

        if "how are you" in question:
            return "I'm doing well. How can I assist you?"

        return (
            "I'm here to help with your documents "
            "or answer general questions."
        )