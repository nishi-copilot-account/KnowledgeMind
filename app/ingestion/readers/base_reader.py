from abc import ABC, abstractmethod

from app.ingestion.models import ParsedDocument


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_path: str) -> ParsedDocument:
        """Read a document and return a ParsedDocument."""
        pass