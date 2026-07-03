"""Markdown document reader module."""

from pathlib import Path

from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeMetadata,
    KnowledgePage,
)

from app.ingestion.readers.base_reader import BaseReader
from app.utils.logger import logger


class MarkdownReader(BaseReader):
    def read(self, file_path: str) -> KnowledgeDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        logger.info("Opening Markdown: %s", path.name)

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as ex:
            logger.error("Unable to open Markdown: %s", ex)
            raise RuntimeError(f"{path.name} is not a valid Markdown document.")

        metadata = KnowledgeMetadata(
            title="",
            author="",
            subject="",
            keywords="",
            page_count=1,
        )

        pages = [
            KnowledgePage(
                page_number=1,
                text=text,
            )
        ]

        logger.info("Markdown Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=pages,
        )
