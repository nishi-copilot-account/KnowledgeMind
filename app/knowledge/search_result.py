"""
Knowledge search result model.
"""

from dataclasses import dataclass

from app.knowledge.chunk import KnowledgeChunk


@dataclass
class KnowledgeSearchResult:
    """
    Represents a semantic search result.
    """

    chunk: KnowledgeChunk

    score: float