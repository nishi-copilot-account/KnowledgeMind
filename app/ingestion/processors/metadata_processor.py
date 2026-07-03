"""
Metadata processor for KnowledgeMind.
"""

from app.knowledge.models import KnowledgeMetadata


class MetadataProcessor:

    def process(self, pdf) -> KnowledgeMetadata:

        metadata = pdf.metadata

        return KnowledgeMetadata(
            title=metadata.get("title", ""),
            author=metadata.get("author", ""),
            subject=metadata.get("subject", ""),
            keywords=metadata.get("keywords", ""),
            page_count=len(pdf),
        )