from abc import ABC, abstractmethod

from app.knowledge.models import KnowledgeDocument
from app.knowledge.chunk import KnowledgeChunk


class ChunkStrategy(ABC):

    @abstractmethod
    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:
        pass