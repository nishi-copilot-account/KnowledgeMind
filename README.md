from dataclasses import dataclass, field
from typing import Any


@dataclass
class KnowledgeMetadata:
    """Metadata associated with a knowledge source."""

    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    source_type: str = ""
    page_count: int = 0


@dataclass
class KnowledgeImage:
    """Image extracted from a knowledge source."""

    page: int
    image_path: str
    ocr_text: str = ""
    caption: str = ""


@dataclass
class KnowledgeTable:
    """Table extracted from a knowledge source."""

    page: int
    rows: list[list[Any]]


@dataclass
class KnowledgePage:
    """Represents one logical page."""

    page_number: int

    text: str = ""

    images: list[KnowledgeImage] = field(default_factory=list)

    tables: list[KnowledgeTable] = field(default_factory=list)


@dataclass
class KnowledgeDocument:
    """Canonical representation of every uploaded knowledge source."""

    source_name: str

    metadata: KnowledgeMetadata

    pages: list[KnowledgePage]