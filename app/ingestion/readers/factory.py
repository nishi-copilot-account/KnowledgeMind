from pathlib import Path

from app.ingestion.readers.pdf_reader import PDFReader
from app.ingestion.readers.docx_reader import DOCXReader
from app.ingestion.readers.txt_reader import TXTReader
from app.ingestion.readers.markdown_reader import MarkdownReader
from app.ingestion.readers.image_reader import ImageReader


class ReaderFactory:
    """
    Factory responsible for selecting the appropriate reader
    based on the input file extension.
    """

    READERS = {
        ".pdf": PDFReader,
        ".docx": DOCXReader,
        ".txt": TXTReader,
        ".md": MarkdownReader,
        ".png": ImageReader,
        ".jpg": ImageReader,
        ".jpeg": ImageReader,
   }

    @classmethod
    def get_reader(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        reader_class = cls.READERS.get(extension)

        if reader_class is None:
            supported = ", ".join(sorted(cls.READERS.keys()))

            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {supported}"
            )

        return reader_class()