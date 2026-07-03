from pathlib import Path

import fitz

from app.knowledge.models import (
    KnowledgeDocument,
    KnowledgeMetadata,
    KnowledgePage,
   )

from app.ingestion.readers.base_reader import BaseReader

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
            #image_processor = ImageProcessor()
            #page_images = image_processor.process(pdf)
        except Exception as ex:
          logger.exception("Unable to open PDF")
          raise RuntimeError(f"{path.name} is not a valid PDF.") from ex

        metadata = KnowledgeMetadata(
            title=pdf.metadata.get("title", ""),
            author=pdf.metadata.get("author", ""),
            subject=pdf.metadata.get("subject", ""),
            keywords=pdf.metadata.get("keywords", ""),
            page_count=len(pdf),
        )

        pages = []

        for index, page in enumerate(pdf):
            pages.append(
                KnowledgePage(
                    page_number=index + 1,
                    text=page.get_text(),
                    #images=page_images.get(index + 1, []),
                    images=[],
                )
            )

        logger.info("PDF Loaded Successfully")

        return KnowledgeDocument(
            filename=path.name,
            metadata=metadata,
            pages=pages,
        )