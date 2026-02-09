from .node import Node
from .edge import Edge

import numpy as np

from typing import List


class Graph:

    def __init__(self, 
        nodes: List[Node], 
        edges: List[Edge],
        bidirectional: bool = True
    ) -> None:
        self.V = len(nodes)
        self.E = len(edges)
        self.nodes = nodes
        self.edges = edges
        self.bidirectional = bidirectional

        self.adj_matrix = dict()
        self.create_adj_matrix()
    
    def create_adj_matrix(self) -> None:
        self.adj_matrix = {node: dict() for node in self.nodes}
        for edge in self.edges:
            self.adj_matrix[edge.start][edge.end] = edge.weight
            if self.bidirectional:
                self.adj_matrix[edge.end][edge.start] = edge.weight

    def get_neighbors(self, node: Node) -> List[Node]:  
        return self.adj_matrix[node].keys()
    
    def get_distance(self, start: Node, end: Node):
        try:
            return self.adj_matrix[start][end]
        except KeyError:
            return np.inf