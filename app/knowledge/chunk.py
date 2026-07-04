"""
Knowledge chunk model.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from app.knowledge.models import (
    KnowledgeImage,
    KnowledgeTable,
)


@dataclass
class KnowledgeChunk:
    """
    Represents the smallest searchable unit of knowledge.
    """

    chunk_id: str

    source_document: str

    source_type: str

    page_number: int

    text: str

    metadata: Dict[str, str] = field(default_factory=dict)

    images: List[KnowledgeImage] = field(default_factory=list)

    tables: List[KnowledgeTable] = field(default_factory=list)