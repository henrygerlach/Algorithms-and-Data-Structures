import numpy as np

from typing import List, Tuple

from data_structures import Node, Graph, Queue


def bfs(
    start: Node, 
    graph: Graph
) -> Tuple[List[int], List[int]]:
    dist, prev, visited = dict(), dict(), dict()
    for node in graph.nodes:
        dist[node] = np.inf
        prev[node] = None
        visited[node] = False
    dist[start] = 0
    visited[start] = True

    queue = Queue([start])

    ##### BFS ALGORITHM #####

    while queue.size:
        nodeX = queue.pop()

        for nodeY in graph.get_neighbors(node=nodeX):
            if visited[nodeY]:
                continue
            visited[nodeY] = True

            queue.insert(nodeY)
            dist[nodeY] = dist[nodeX] + 1
            prev[nodeY] = nodeX
    
    return dist, prev