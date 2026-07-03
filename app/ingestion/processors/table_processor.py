from PIL import Image

import pytesseract


class OCRProcessor:

    def process(self, image_path):

        image = Image.open(image_path)

        return pytesseract.image_to_string(image)
