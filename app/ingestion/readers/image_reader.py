"""
Image document reader.
"""

from pathlib import Path

from app.ingestion.processors.ocr_processor import OCRProcessor
from app.ingestion.readers.base_reader import BaseReader
from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeImage,
    KnowledgeMetadata,
    KnowledgePage,
)
from app.utils.logger import logger


class ImageReader(BaseReader):
    """
    Reads image documents (PNG, JPG, JPEG).
    """

    def read(self, file_path: str) -> KnowledgeDocument:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if path.stat().st_size == 0:
            raise ValueError(f"{path.name} is empty.")

        logger.info("Opening Image : %s", path.name)

        ocr_processor = OCRProcessor()

        ocr_text = ocr_processor.process(str(path))

        metadata = KnowledgeMetadata(
            title=path.stem,
            page_count=1,
        )

        page = KnowledgePage(
            page_number=1,
            text=ocr_text,
            images=[
                KnowledgeImage(
                    page=1,
                    path=str(path),
                    ocr_text=ocr_text,
                )
            ],
        )

        logger.info("Image Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=[page],
        )