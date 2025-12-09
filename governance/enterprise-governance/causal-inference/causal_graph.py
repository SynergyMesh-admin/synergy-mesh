#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Causal Graph Module

Implements causal graph data structures and operations for governance decisions.
Supports:
- Causal relationships between governance entities
- Forward inference (cause → effect)
- Backward inference (effect → cause)
- Intervention analysis (what if we change this?)
- Counterfactual analysis (what if we had decided differently?)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum
import json
from pathlib import Path


class CausalRelationType(Enum):
    """Types of causal relationships"""
    DIRECT = "direct"              # A directly causes B
    INDIRECT = "indirect"          # A → ... → B
    CONFOUNDED = "confounded"      # A and B both caused by C
    BIDIRECTIONAL = "bidirectional" # A ↔ B (feedback loop)
    CONDITIONAL = "conditional"    # A causes B only if C is true


@dataclass
class CausalEdge:
    """Represents a causal relationship between two variables"""
    source: str                    # Source node (cause)
    target: str                    # Target node (effect)
    relation_type: CausalRelationType
    strength: float               # Strength (0-1, where 1 is strongest)
    latency_ms: int              # How long for effect to manifest
    reversible: bool             # Can effect be reversed by reversing cause?
    confidence: float            # Confidence in this causal relationship (0-1)
    evidence: List[str]          # Evidence supporting this relationship
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source": self.source,
            "target": self.target,
            "relation_type": self.relation_type.value,
            "strength": self.strength,
            "latency_ms": self.latency_ms,
            "reversible": self.reversible,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "metadata": self.metadata
        }


@dataclass
class CausalNode:
    """Represents a governance variable in the causal graph"""
    name: str
    node_type: str              # "decision", "risk", "outcome", "resource"
    description: str
    domain: str                 # governance dimension
    possible_values: List[str]  # possible states
    current_value: Optional[str] = None
    probability_distribution: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "node_type": self.node_type,
            "description": self.description,
            "domain": self.domain,
            "possible_values": self.possible_values,
            "current_value": self.current_value,
            "probability_distribution": self.probability_distribution,
            "metadata": self.metadata
        }


class CausalGraph:
    """Represents governance causal relationships as a directed acyclic graph"""

    def __init__(self, name: str = "GovernanceCausalGraph"):
        """Initialize causal graph"""
        self.name = name
        self.nodes: Dict[str, CausalNode] = {}
        self.edges: List[CausalEdge] = []
        self._node_edges_cache: Dict[str, Tuple[List[CausalEdge], List[CausalEdge]]] = {}

    def add_node(self, node: CausalNode) -> None:
        """Add a node to the graph"""
        if node.name in self.nodes:
            raise ValueError(f"Node {node.name} already exists")
        self.nodes[node.name] = node
        self._invalidate_cache()

    def add_edge(self, edge: CausalEdge) -> None:
        """Add a causal edge to the graph"""
        if edge.source not in self.nodes:
            raise ValueError(f"Source node {edge.source} not found")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node {edge.target} not found")

        # Check for cycles in case of DIRECT relationships
        if edge.relation_type == CausalRelationType.DIRECT:
            if self._would_create_cycle(edge.source, edge.target):
                raise ValueError(f"Adding edge {edge.source} → {edge.target} would create a cycle")

        self.edges.append(edge)
        self._invalidate_cache()

    def remove_edge(self, source: str, target: str) -> bool:
        """Remove an edge from the graph"""
        initial_count = len(self.edges)
        self.edges = [e for e in self.edges if not (e.source == source and e.target == target)]
        if len(self.edges) < initial_count:
            self._invalidate_cache()
            return True
        return False

    def get_parents(self, node_name: str) -> List[str]:
        """Get all parent nodes (direct causes)"""
        return [e.source for e in self.edges if e.target == node_name and e.relation_type == CausalRelationType.DIRECT]

    def get_children(self, node_name: str) -> List[str]:
        """Get all child nodes (direct effects)"""
        return [e.target for e in self.edges if e.source == node_name and e.relation_type == CausalRelationType.DIRECT]

    def get_ancestors(self, node_name: str) -> Set[str]:
        """Get all ancestor nodes (all causes, direct and indirect)"""
        ancestors: Set[str] = set()
        to_visit = self.get_parents(node_name)

        while to_visit:
            current = to_visit.pop(0)
            if current not in ancestors:
                ancestors.add(current)
                to_visit.extend(self.get_parents(current))

        return ancestors

    def get_descendants(self, node_name: str) -> Set[str]:
        """Get all descendant nodes (all effects, direct and indirect)"""
        descendants: Set[str] = set()
        to_visit = self.get_children(node_name)

        while to_visit:
            current = to_visit.pop(0)
            if current not in descendants:
                descendants.add(current)
                to_visit.extend(self.get_children(current))

        return descendants

    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        """Find a causal path from source to target"""
        if source == target:
            return [source]

        visited: Set[str] = set()
        queue: List[Tuple[str, List[str]]] = [(source, [source])]

        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for child in self.get_children(current):
                if child == target:
                    return path + [child]
                if child not in visited:
                    queue.append((child, path + [child]))

        return None

    def find_all_paths(self, source: str, target: str) -> List[List[str]]:
        """Find all causal paths from source to target"""
        def dfs(current: str, target: str, path: List[str], visited: Set[str]) -> List[List[str]]:
            if current == target:
                return [path]

            paths = []
            for child in self.get_children(current):
                if child not in visited:
                    new_visited = visited.copy()
                    new_visited.add(child)
                    paths.extend(dfs(child, target, path + [child], new_visited))

            return paths

        return dfs(source, target, [source], {source})

    def get_confounders(self, node1: str, node2: str) -> Set[str]:
        """Find common ancestors (confounders) of two nodes"""
        ancestors1 = self.get_ancestors(node1)
        ancestors2 = self.get_ancestors(node2)
        return ancestors1.intersection(ancestors2)

    def is_confounder(self, potential_confounder: str, node1: str, node2: str) -> bool:
        """Check if a node is a confounder for two other nodes"""
        confounders = self.get_confounders(node1, node2)
        return potential_confounder in confounders

    def _would_create_cycle(self, source: str, target: str) -> bool:
        """Check if adding an edge would create a cycle"""
        # An edge from source to target creates a cycle if target can reach source
        descendants = self.get_descendants(target)
        return source in descendants

    def _invalidate_cache(self) -> None:
        """Invalidate internal caches"""
        self._node_edges_cache.clear()

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the causal graph for consistency"""
        errors: List[str] = []

        # Check for bidirectional cycles (should be marked as BIDIRECTIONAL, not DIRECT)
        for node in self.nodes:
            if self._has_unintended_cycle(node):
                errors.append(f"Potential unintended cycle involving {node}")

        # Check for isolated nodes (optional)
        for node_name, node in self.nodes.items():
            if not self.get_parents(node_name) and not self.get_children(node_name):
                errors.append(f"Node {node_name} is isolated (no relationships)")

        return len(errors) == 0, errors

    def _has_unintended_cycle(self, start_node: str) -> bool:
        """Check if there's an unintended cycle from a node"""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for child in self.get_children(node):
                if child not in visited:
                    if dfs(child):
                        return True
                elif child in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        return dfs(start_node)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "nodes": {name: node.to_dict() for name, node in self.nodes.items()},
            "edges": [edge.to_dict() for edge in self.edges]
        }

    def to_json(self, file_path: Path) -> None:
        """Save to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CausalGraph':
        """Create from dictionary"""
        graph = CausalGraph(data.get("name", "GovernanceCausalGraph"))

        # Add nodes
        for node_data in data.get("nodes", {}).values():
            node = CausalNode(
                name=node_data["name"],
                node_type=node_data["node_type"],
                description=node_data["description"],
                domain=node_data["domain"],
                possible_values=node_data["possible_values"],
                current_value=node_data.get("current_value"),
                probability_distribution=node_data.get("probability_distribution", {}),
                metadata=node_data.get("metadata", {})
            )
            graph.add_node(node)

        # Add edges
        for edge_data in data.get("edges", []):
            edge = CausalEdge(
                source=edge_data["source"],
                target=edge_data["target"],
                relation_type=CausalRelationType(edge_data["relation_type"]),
                strength=edge_data["strength"],
                latency_ms=edge_data["latency_ms"],
                reversible=edge_data["reversible"],
                confidence=edge_data["confidence"],
                evidence=edge_data["evidence"],
                metadata=edge_data.get("metadata", {})
            )
            graph.add_edge(edge)

        return graph

    def __str__(self) -> str:
        """String representation"""
        return f"CausalGraph({self.name}): {len(self.nodes)} nodes, {len(self.edges)} edges"

    def __repr__(self) -> str:
        """Detailed representation"""
        return self.__str__()
