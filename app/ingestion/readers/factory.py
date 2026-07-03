from pathlib import Path

from app.ingestion.readers.pdf_reader import PDFReader
from app.ingestion.readers.docx_reader import DOCXReader
from app.ingestion.readers.txt_reader import TXTReader
from app.ingestion.readers.markdown_reader import MarkdownReader


class ReaderFactory:

    READERS = {
        ".pdf": PDFReader,
        ".docx": DOCXReader,
        ".txt": TXTReader,
        ".md": MarkdownReader,
    }

    @classmethod
    def get_reader(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        reader = cls.READERS.get(extension)

        if reader is None:
            raise ValueError(
                f"No reader registered for '{extension}'"
            )

        return reader()