from pathlib import Path

import fitz

from app.knowledge.models import KnowledgeImage
from app.utils.logger import logger


class ImageProcessor:

    def __init__(self):

        self.output_folder = Path("data/extracted_images")

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

    def process(self, pdf):

        extracted = {}

        for page_number in range(len(pdf)):

            page = pdf[page_number]

            images = []

            image_list = page.get_images(full=True)

            logger.info(
                "Page %s -> %s image(s)",
                page_number + 1,
                len(image_list),
            )

            for index, image in enumerate(image_list):

                xref = image[0]

                pix = fitz.Pixmap(pdf, xref)

                if pix.alpha:
                    pix = fitz.Pixmap(
                        fitz.csRGB,
                        pix,
                    )

                image_name = (
                    f"page_{page_number+1}_{index+1}.png"
                )

                image_path = (
                    self.output_folder / image_name
                )

                pix.save(image_path)

                pix = None

                images.append(
    {
        "page": page_number + 1,
        "image_path": str(image_path),
    }
)

            extracted[page_number + 1] = images

        return extracted
