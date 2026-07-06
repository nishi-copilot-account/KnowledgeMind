"""
State shared across the LangGraph workflow.
"""

from typing import TypedDict

from app.knowledge.search_result import KnowledgeSearchResult


class KnowledgeState(TypedDict, total=False):
    """
    Shared state passed between all LangGraph nodes.
    """

    # Original user question
    original_question: str

    # Current question (may be rewritten)
    question: str

    # Retrieved search results
    search_results: list[KnowledgeSearchResult]

    # Prepared context for the LLM
    context: str

    # Final answer
    answer: str

    # Planner action
    action: str

    # Extracted entities (optional)
    entities: dict

    # Conversation history
    history: str

    # Workflow execution trace
    workflow_steps: list[str]