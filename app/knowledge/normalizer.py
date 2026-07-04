"""
Knowledge document normalizer.

Converts a KnowledgeDocument into searchable KnowledgeChunks.
"""

import uuid

from app.knowledge.chunk import KnowledgeChunk
from app.knowledge.models import KnowledgeDocument


class KnowledgeNormalizer:
    """
    Converts documents into knowledge chunks.
    """

    def normalize(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:

        chunks = []

        for page in document.pages:

            chunk = KnowledgeChunk(
                chunk_id=str(uuid.uuid4()),
                source_document=document.filename,
                source_type=document.filename.split(".")[-1].lower(),
                page_number=page.page_number,
                text=page.text,
                metadata={
                    "title": document.metadata.title,
                    "author": document.metadata.author,
                },
                images=page.images,
                tables=page.tables,
            )

            chunks.append(chunk)

        return chunks