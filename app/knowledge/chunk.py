"""Text chunking strategies and utilities."""

from dataclasses import dataclass
from typing import List
from enum import Enum


class ChunkStrategy(Enum):
    """Chunking strategies for text."""

    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"
    SLIDING_WINDOW = "sliding_window"


@dataclass
class TextChunk:
    """Represents a chunk of text."""

    content: str
    chunk_id: str
    source_document: str
    start_index: int
    end_index: int
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ChunkProcessor:
    """Process and create text chunks."""

    @staticmethod
    def create_fixed_size_chunks(
        text: str, chunk_size: int = 1024, overlap: int = 100
    ) -> List[TextChunk]:
        """Create fixed-size text chunks with overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]

            chunk = TextChunk(
                content=chunk_text,
                chunk_id=f"chunk_{start}_{end}",
                source_document="",
                start_index=start,
                end_index=end,
            )
            chunks.append(chunk)
            start = end - overlap

        return chunks

    @staticmethod
    def create_semantic_chunks(text: str) -> List[TextChunk]:
        """Create semantically meaningful chunks."""
        # Implementation for semantic chunking
        chunks = []
        return chunks
