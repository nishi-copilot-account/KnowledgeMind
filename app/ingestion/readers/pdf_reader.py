from pathlib import Path

import fitz

from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeMetadata,
    KnowledgePage,
)

from app.ingestion.readers.base_reader import BaseReader
from app.ingestion.processors.metadata_processor import MetadataProcessor
from app.ingestion.processors.text_processor import TextProcessor
from app.ingestion.processors.image_processor import ImageProcessor
print("DEBUG: ImageProcessor =", ImageProcessor)

from app.utils.logger import logger


class PDFReader(BaseReader):
    def read(self, file_path: str) -> KnowledgeDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if path.stat().st_size < 100:
            raise ValueError(f"{path.name} is too small to be a valid PDF.")

        logger.info("Opening PDF : %s", path.name)

        if path.stat().st_size == 0:
            raise ValueError("PDF file is empty.")

        try:
            pdf = fitz.open(path)
            
        except Exception as ex:
            logger.exception("Unable to open PDF")
            raise RuntimeError(f"{path.name} is not a valid PDF.") from ex

            # Processors run after the PDF is successfully opened
         # Initialize processors   
        metadata_processor = MetadataProcessor()
        text_processor = TextProcessor()
        image_processor = ImageProcessor()

        # Process metadata
        metadata = metadata_processor.process(pdf)
        # Process images
        page_images = image_processor.process(pdf)

        
        pages = []

        for index, page in enumerate(pdf):
            raw_text = page.get_text()
            clean_text = text_processor.process(raw_text)
            pages.append(
                KnowledgePage(
                    page_number=index + 1,
                    text=clean_text,
                    images=page_images.get(index + 1, []),
                    
                )
            )

        logger.info("PDF Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=pages,
        )