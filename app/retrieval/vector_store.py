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

    # --------------------------------------------------
    # Add
    # --------------------------------------------------

    def add(
        self,
        chunk: KnowledgeChunk,
        embedding: list[float],
    ) -> None:

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

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        source_document: str | None = None,
    ):
        """
        Search for the most similar knowledge chunks.
        """

        logger.info(
            "Searching vector store (top_k=%s)",
            top_k,
        )

        query = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }

        if source_document:

            logger.info(
                "Filtering search by document: %s",
                source_document,
            )

            query["where"] = {
                "source_document": source_document,
            }

            print("=" * 60)
            print("CHROMA QUERY =", query)
            print("=" * 60)

        results = self.collection.query(**query)
        print("=" * 60)

        print("Retrieved Documents")

        for metadata in results["metadatas"][0]:
            print(metadata["source_document"])

        print("=" * 60)

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

    # --------------------------------------------------
    # Document Exists
    # --------------------------------------------------

    def document_exists(
        self,
        document_name: str,
    ) -> bool:

        results = self.collection.get(
            where={
                "source_document": document_name,
            }
        )

        return len(results["ids"]) > 0

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self) -> dict:

        results = self.collection.get()

        metadatas = results["metadatas"]

        documents = sorted(
            {
                metadata["source_document"]
                for metadata in metadatas
            }
        )

        return {
            "documents": documents,
            "document_count": len(documents),
            "chunk_count": len(results["ids"]),
        }