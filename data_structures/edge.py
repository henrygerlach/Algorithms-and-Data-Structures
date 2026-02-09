from .node import Node

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Edge:
    start: Node
    end: Node
    weight: float = 1.0