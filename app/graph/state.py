"""
State shared across the LangGraph workflow.
"""

from typing import TypedDict

from app.knowledge.search_result import KnowledgeSearchResult


class KnowledgeState(TypedDict, total=False):

    original_question: str

    question: str

    search_results: list[KnowledgeSearchResult]

    context: str

    answer: str

    action: str

    entities: dict

    history: str

    workflow_steps: list[str]

    selected_document: str

    explanation: list[str]