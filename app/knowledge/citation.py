"""Citation and source tracking utilities."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Citation:
    """Represents a citation to a source."""

    source_document: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    confidence_score: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SourceReference:
    """References to source documents."""

    reference_id: str
    document_name: str
    document_path: str
    citations: List[Citation] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class CitationManager:
    """Manages citations and source references."""

    def __init__(self):
        self.citations: List[Citation] = []
        self.source_references: dict = {}

    def add_citation(self, citation: Citation) -> None:
        """Add a citation."""
        self.citations.append(citation)

    def add_source_reference(self, reference: SourceReference) -> None:
        """Add a source reference."""
        self.source_references[reference.reference_id] = reference

    def get_citations_for_source(self, source_document: str) -> List[Citation]:
        """Get all citations for a specific source document."""
        return [c for c in self.citations if c.source_document == source_document]

    def generate_citation_string(self, citation: Citation) -> str:
        """Generate a formatted citation string."""
        parts = [citation.source_document]

        if citation.page_number:
            parts.append(f"p. {citation.page_number}")

        if citation.section:
            parts.append(f"Section: {citation.section}")

        return " - ".join(parts)
