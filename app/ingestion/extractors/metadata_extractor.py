import fitz

from app.ingestion.models import DocumentMetadata


class MetadataExtractor:

    def extract(self, pdf):

        metadata = pdf.metadata

        return DocumentMetadata(

            title=metadata.get("title", ""),

            author=metadata.get("author", ""),

            subject=metadata.get("subject", ""),

            keywords=metadata.get("keywords", ""),

            page_count=len(pdf),
        )