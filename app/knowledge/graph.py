"""Knowledge graph construction and operations."""

from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Node:
    """Represents a node in the knowledge graph."""

    id: str
    label: str
    properties: Dict = field(default_factory=dict)


@dataclass
class Edge:
    """Represents an edge between nodes."""

    source_id: str
    target_id: str
    relation_type: str
    properties: Dict = field(default_factory=dict)


class GraphConstructor:
    """Constructs and manages knowledge graphs."""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        if edge.source_id in self.nodes and edge.target_id in self.nodes:
            self.edges.append(edge)

    def get_neighbors(self, node_id: str) -> List[Node]:
        """Get all neighboring nodes."""
        neighbors = []
        for edge in self.edges:
            if edge.source_id == node_id:
                neighbors.append(self.nodes[edge.target_id])
        return neighbors

    def get_graph_json(self) -> Dict:
        """Export graph as JSON."""
        return {
            "nodes": [
                {"id": n.id, "label": n.label, "properties": n.properties}
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "relation": e.relation_type,
                    "properties": e.properties,
                }
                for e in self.edges
            ],
        }
