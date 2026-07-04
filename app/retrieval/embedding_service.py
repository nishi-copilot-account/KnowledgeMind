"""
Embedding service for KnowledgeMind.
"""

from sentence_transformers import SentenceTransformer
from app.utils.logger import logger

class EmbeddingService:
    """
    Generates vector embeddings for text.
    """

    _model = None

    def __init__(self):

        if EmbeddingService._model is None:
            logger.info("Loading embedding model...")
            EmbeddingService._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

    def embed(self, text: str) -> list[float]:

        vector = EmbeddingService._model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()