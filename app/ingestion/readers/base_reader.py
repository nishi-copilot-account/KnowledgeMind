from abc import ABC, abstractmethod

from app.knowledge.models import KnowledgeDocument


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_path: str) -> KnowledgeDocument:
        """
        Reads any knowledge source and returns
        a canonical KnowledgeDocument.
        """
        raise NotImplementedError