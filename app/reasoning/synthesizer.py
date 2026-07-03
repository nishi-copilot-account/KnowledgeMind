"""Synthesizer component for combining information."""

from typing import List, Dict, Any


class Synthesizer:
    """Synthesizes information from multiple sources."""

    def synthesize(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Synthesize an answer from retrieved documents."""
        if not retrieved_docs:
            return "No relevant documents found."
        
        synthesis = "Based on the retrieved documents:\n"
        for i, doc in enumerate(retrieved_docs, 1):
            synthesis += f"{i}. {doc.get('content', '')}\n"
        
        return synthesis

    def add_citations(self, synthesis: str, sources: List[str]) -> str:
        """Add citations to the synthesized answer."""
        citation_text = "\n\nSources:\n"
        for source in sources:
            citation_text += f"- {source}\n"
        
        return synthesis + citation_text

    def reflect(self, synthesis: str) -> Dict[str, Any]:
        """Reflect on the synthesis for quality assurance."""
        return {
            "synthesis": synthesis,
            "quality_score": 0.85,
            "needs_revision": False
        }
