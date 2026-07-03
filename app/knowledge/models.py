"""Knowledge models and data structures."""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class KnowledgeImage:
    """Represents an extracted image from a document."""

    page: int
    path: str
    ocr_text: str = ""


@dataclass
class KnowledgeTable:
    """
    Represents a table extracted from a document.
    """

    page: int

    title: str = ""
    rows: List[List[str]] = field(default_factory=list)

@dataclass
class KnowledgePage:

    page_number: int

    text: str

    images: List[KnowledgeImage] = field(default_factory=list)

    tables: List[KnowledgeTable] = field(default_factory=list)


@dataclass
class KnowledgeMetadata:
    """Metadata for a knowledge document."""

    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    page_count: int = 0


@dataclass
class KnowledgeDocument:
    """Represents a parsed knowledge document."""

    filename: str
    metadata: KnowledgeMetadata
    pages: List[KnowledgePage]


@dataclass
class KnowledgeEntity:
    """Base knowledge entity."""

    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeGraph:
    """Knowledge graph representation."""

    entities: List[KnowledgeEntity] = field(default_factory=list)
    relationships: List[dict] = field(default_factory=list)

    def add_entity(self, entity: KnowledgeEntity) -> None:
        """Add entity to knowledge graph."""
        self.entities.append(entity)

    def add_relationship(self, source_id: str, target_id: str, relation_type: str) -> None:
        """Add relationship between entities."""
        self.relationships.append({
            "source": source_id,
            "target": target_id,
            "type": relation_type,
        })
