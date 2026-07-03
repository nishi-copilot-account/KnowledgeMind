"""
OCR Processor for KnowledgeMind.

Extracts text from images using Tesseract OCR.
"""

from pathlib import Path

import pytesseract
from PIL import Image

from app.config.settings import TESSERACT_PATH


class OCRProcessor:

    def __init__(self):

        pytesseract.pytesseract.tesseract_cmd = str(
            TESSERACT_PATH
        )

    def process(self, image_path: str) -> str:
        """
        Extract text from an image.
        """

        image = Image.open(Path(image_path))

        text = pytesseract.image_to_string(image)

        return text.strip()