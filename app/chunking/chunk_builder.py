"""
Chunk builder.
"""

from app.chunking.base_strategy import ChunkStrategy
from app.chunking.page_strategy import PageChunkStrategy
from app.knowledge.chunk import KnowledgeChunk
from app.knowledge.models import KnowledgeDocument


class ChunkBuilder:
    """
    Builds knowledge chunks using a strategy.
    """

    def __init__(
        self,
        strategy: ChunkStrategy | None = None,
    ):

        self.strategy = strategy or PageChunkStrategy()

    def build(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:

        return self.strategy.chunk(document)