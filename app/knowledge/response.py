"""
Knowledge response model.
"""

from dataclasses import dataclass, field

from app.knowledge.search_result import KnowledgeSearchResult


@dataclass
class KnowledgeResponse:
    """
    Final response returned to the UI.
    """

    answer: str

    sources: list[KnowledgeSearchResult] = field(default_factory=list)

    workflow: list[str] = field(default_factory=list)

    explanation: list[str] = field(default_factory=list)