"""
Page-based chunking strategy.
"""

import uuid

from app.chunking.base_strategy import ChunkStrategy
from app.knowledge.chunk import KnowledgeChunk
from app.knowledge.models import KnowledgeDocument


class PageChunkStrategy(ChunkStrategy):
    """
    Creates one chunk per page.
    """

    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:

        chunks = []

        for page in document.pages:

            chunk = KnowledgeChunk(
                chunk_id=str(uuid.uuid4()),
                source_document=document.filename,
                source_type=document.filename.split(".")[-1],
                page_number=page.page_number,
                text=page.text,
                images=page.images,
                tables=page.tables,
            )

            chunks.append(chunk)

        return chunks