"""
Extract images from PDF pages.
"""
from app.ingestion.processors.ocr_processor import OCRProcessor
from pathlib import Path
from app.knowledge.models import KnowledgeImage

import fitz


class ImageProcessor:

    def __init__(self):

        self.output_dir = Path("data/extracted_images")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.ocr_processor = OCRProcessor()

    def process(self, pdf):

        page_images = {}

        for page_index in range(len(pdf)):

            page = pdf[page_index]

            extracted = []

            image_list = page.get_images(full=True)

            for image_number, image in enumerate(image_list):

                xref = image[0]

                pix = fitz.Pixmap(pdf, xref)

                if pix.alpha:

                    pix = fitz.Pixmap(
                        fitz.csRGB,
                        pix,
                    )

                image_name = (
                    f"page_{page_index+1}_{image_number+1}.png"
                )

                image_path = (
                    self.output_dir / image_name
                )

                pix.save(image_path)

                pix = None
                ocr_text = self.ocr_processor.process(str(image_path))
                extracted.append(
                    KnowledgeImage(
                        page=page_index + 1,
                        path=str(image_path),
                        ocr_text=ocr_text,
                    )
                )

            page_images[page_index + 1] = extracted

        return page_images