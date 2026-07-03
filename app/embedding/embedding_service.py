"""Embedding and vector representation utilities."""

from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass
class Embedding:
    """Represents an embedding vector."""

    text: str
    vector: List[float]
    model: str
    dimension: int

    def __post_init__(self):
        self.dimension = len(self.vector)


class EmbeddingService:
    """Service for managing embeddings and similarity operations."""

    def __init__(self, model_name: str = "sentence-transformers"):
        self.model_name = model_name
        self.embeddings: List[Embedding] = []

    def add_embedding(self, embedding: Embedding) -> None:
        """Add an embedding to the collection."""
        self.embeddings.append(embedding)

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

    def find_similar(self, query_vector: List[float], top_k: int = 5) -> List[tuple]:
        """Find top-k most similar embeddings."""
        similarities = []
        
        for embedding in self.embeddings:
            sim = self.cosine_similarity(query_vector, embedding.vector)
            similarities.append((embedding.text, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
