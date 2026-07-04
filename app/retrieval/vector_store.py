"""
Vector store implementation using ChromaDB.
"""

import chromadb

from app.knowledge.chunk import KnowledgeChunk
from app.knowledge.search_result import KnowledgeSearchResult
from app.utils.logger import logger


class VectorStore:
    """
    Stores and retrieves knowledge chunks using ChromaDB.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledgemind"
        )

    def add(
        self,
        chunk: KnowledgeChunk,
        embedding: list[float],
    ) -> None:
        """
        Store a knowledge chunk in ChromaDB.
        """

        self.collection.add(
            ids=[chunk.chunk_id],

            embeddings=[embedding],

            documents=[chunk.text],

            metadatas=[
                {
                    "source_document": chunk.source_document,
                    "source_type": chunk.source_type,
                    "page_number": chunk.page_number,
                }
            ],
        )

        logger.info(
            "Stored chunk %s",
            chunk.chunk_id,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ):
        """
        Search for the most similar knowledge chunks.
        """

        logger.info(
            "Searching vector store (top_k=%s)",
            top_k,
        )

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        search_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        for i in range(len(documents)):

            metadata = metadatas[i]

            chunk = KnowledgeChunk(
                chunk_id=ids[i],
                source_document=metadata["source_document"],
                source_type=metadata["source_type"],
                page_number=metadata["page_number"],
                text=documents[i],
                metadata={},
                images=[],
                tables=[],
            )

            search_results.append(
                KnowledgeSearchResult(
                    chunk=chunk,
                    score=distances[i],
                )
            )

        return search_results