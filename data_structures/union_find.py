from typing import List
from dataclasses import dataclass

from .graph import Node


@dataclass
class Subset():
    rank: int
    parent: Node


class UnionFind():

    def __init__(
        self, 
        nodes: List[Node],
        subsets: List[Subset] = None
    ) -> None:
        self.nodes = nodes
        self.subsets = subsets
    
    def make_sets(self):
        self.subsets = {node: Subset(0, node) for node in self.nodes}

    def find(self, node: Node) -> Node:
        if self.subsets[node].parent.val == node.val:
            return node
        return self.find(self.subsets[node].parent)

    def union(self, x: Node, y: Node):
        xRoot = self.find(x)
        yRoot = self.find(y)

        if self.subsets[xRoot].rank < self.subsets[yRoot].rank:
            self.subsets[xRoot].parent = yRoot
        elif self.subsets[xRoot].rank > self.subsets[yRoot].rank:
            self.subsets[yRoot].parent = xRoot
        else:
            self.subsets[yRoot].parent = xRoot
            self.subsets[xRoot].rank += 1