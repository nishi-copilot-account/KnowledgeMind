import os
import fitz

from app.ingestion.models import DocumentImage


class ImageExtractor:

    def extract(self, page, page_number, output_folder):

        images = []

        image_list = page.get_images(full=True)

        os.makedirs(output_folder, exist_ok=True)

        for index, image in enumerate(image_list):

            xref = image[0]

            pix = fitz.Pixmap(page.parent, xref)

            image_name = f"page_{page_number}_{index}.png"

            image_path = os.path.join(output_folder, image_name)

            if pix.alpha:

                pix = fitz.Pixmap(fitz.csRGB, pix)

            pix.save(image_path)

            pix = None

            images.append(

                DocumentImage(

                    page=page_number,

                    image_path=image_path,

                )

            )

        return images