"""DOCX document reader module."""

from pathlib import Path

from docx import Document

from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeMetadata,
    KnowledgePage,
)

from app.ingestion.readers.base_reader import BaseReader
from app.utils.logger import logger


class DOCXReader(BaseReader):
    def read(self, file_path: str) -> KnowledgeDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        logger.info("Opening DOCX: %s", path.name)

        try:
            doc = Document(path)
        except Exception as ex:
            logger.error("Unable to open DOCX: %s", ex)
            raise RuntimeError(f"{path.name} is not a valid DOCX document.")

        metadata = KnowledgeMetadata(
            title=doc.core_properties.title or "",
            author=doc.core_properties.author or "",
            subject=doc.core_properties.subject or "",
            keywords=doc.core_properties.keywords or "",
            page_count=len(doc.paragraphs),
        )

        pages = []
        text_content = []

        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)

        pages.append(
            KnowledgePage(
                page_number=1,
                text="\n".join(text_content),
            )
        )

        logger.info("DOCX Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=pages,
        )
