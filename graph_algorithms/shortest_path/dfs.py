import numpy as np

from typing import List, Tuple

from data_structures import Node, Graph, Stack


def dfs(start: Node, graph: Graph) -> Tuple[List[int], List[int]]:
    dist, prev, visited = dict(), dict(), dict()
    for node in graph.nodes:
        dist[node] = np.inf
        prev[node] = None
        visited[node] = False
    dist[start] = 0

    stack = Stack([start])

    ##### DFS ALGORITHM #####

    while stack.size:
        nodeX = stack.pop()

        if visited[nodeX]:
            continue
        visited[nodeX] = True

        for nodeY in graph.get_neighbors(node=nodeX):
            if visited[nodeY]:
                continue

            stack.add(nodeY)
            dist[nodeY] = dist[nodeX] + 1
            prev[nodeY] = nodeX

    return dist, prev
