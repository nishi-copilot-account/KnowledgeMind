"""
Plain text document reader.
"""

from pathlib import Path

from app.ingestion.readers.base_reader import BaseReader
from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeMetadata,
    KnowledgePage,
)
from app.utils.logger import logger


class TXTReader(BaseReader):
    """
    Reads plain text (.txt) documents.
    """

    def read(self, file_path: str) -> KnowledgeDocument:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if path.stat().st_size == 0:
            raise ValueError(f"{path.name} is empty.")

        logger.info("Opening TXT : %s", path.name)

        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        metadata = KnowledgeMetadata(
            title=path.stem,
            page_count=1,
        )

        page = KnowledgePage(
            page_number=1,
            text=text,
        )

        logger.info("TXT Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=[page],
        )