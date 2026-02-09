import numpy as np

from data_structures import MinHeap, Graph, Node

from typing import Tuple, Dict 


def dijkstra(
    start: Node, 
    graph: Graph
) -> Tuple[Dict[any, float], Dict[any, any]]:
    prev, dist, visited = dict(), dict(), dict()
    for node in graph.nodes:
        prev[node] = None
        dist[node] = np.inf
        visited[node] = False
    dist[start] = 0

    min_heap = MinHeap(
        heap=[(0, start)] + 
        [(np.inf, node) for node in graph.nodes if node != start]
    )

    ##### DIJKSTRA ALGORITHM #####

    while min_heap.heap:
        distX, nodeX = min_heap.get_min()
        visited[nodeX.val] = True

        for nodeY in graph.adj_matrix[nodeX]:
            if visited[nodeY]:
                continue
            
            distXY = distX + graph.get_distance(nodeX, nodeY)
            distY = dist[nodeY]

            if distXY < distY:
                min_heap.decrease_key(new_prio=distXY, key=(distY, nodeY))
                dist[nodeY] = distXY
                prev[nodeY] = nodeX
    
    return dist, prev