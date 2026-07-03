"""
Extract images from PDF pages.
"""

from pathlib import Path

import fitz


class ImageProcessor:

    def __init__(self):

        self.output_dir = Path("data/extracted_images")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

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

                extracted.append(
                    {
                        "page": page_index + 1,
                        "path": str(image_path),
                    }
                )

            page_images[page_index + 1] = extracted

        return page_images