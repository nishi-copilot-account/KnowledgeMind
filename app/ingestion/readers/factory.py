from pathlib import Path

from app.ingestion.readers.pdf_reader import PDFReader


class ReaderFactory:

    @staticmethod
    def get_reader(file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return PDFReader()

        raise ValueError(f"Unsupported file type: {extension}")