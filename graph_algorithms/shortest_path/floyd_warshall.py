import copy
import numpy as np

from typing import Dict

from data_structures import Graph, Node


def floyd_warshall(graph: Graph) -> Dict[int, Dict[int, float]]:
    def _get_distance(start: Node, end: Node):
        try:
            return dist[start][end]
        except KeyError:
            return np.inf

    dist = copy.deepcopy(graph.adj_matrix)

    ##### FLOYD WARSHALL ALGORITHM #####

    for nodeK in graph.nodes:
        for nodeI in graph.nodes:
            for nodeJ in graph.nodes:
                dist[nodeI][nodeJ] = min(
                    _get_distance(nodeI, nodeJ),
                    _get_distance(nodeI, nodeK) + _get_distance(nodeK, nodeJ),
                )

    return dist
