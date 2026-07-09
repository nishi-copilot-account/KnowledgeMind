from abc import ABC, abstractmethod

from app.knowledge.models import KnowledgeDocument


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_path: str, original_filename: str | None = None,) -> KnowledgeDocument:
        """
        Reads any knowledge source and returns
        a canonical KnowledgeDocument.
        """
        raise NotImplementedError