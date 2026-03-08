import copy

from typing import Tuple, List

from data_structures import Graph, Edge
from graph_algorithms import kruskal


def tsp_mst(graph: Graph) -> Tuple[float, List[int]]:
    optRoute = []
    optValue = float("inf")

    def _B(route: List[int]):
        k = len(route)
        cur = sum(graph.get_distance(route[i], route[i + 1]) for i in range(k - 1))
        V = list(set(graph.nodes).difference(set(route[1:-1])))
        E = [
            Edge(s, e, w)
            for s, es in graph.adj_matrix.items()
            for e, w in es.items()
            if e in V and s in V
        ]
        G = Graph(nodes=V, edges=E, bidirectional=True)
        mst = kruskal(G)
        return cur + sum(edge.weight for edge in mst)

    def _backtrack(k: int, route: List[int]):
        nonlocal optValue
        nonlocal optRoute

        if k == graph.V:
            curValue = sum(
                graph.get_distance(route[i], route[i + 1]) for i in range(k - 1)
            ) + graph.get_distance(route[k - 1], route[0])
            if curValue < optValue:
                optValue = curValue
                optRoute = copy.deepcopy(route)
        else:
            for node in list(set(graph.nodes).difference(set(route))):
                if _B(route) < optValue:
                    _backtrack(k + 1, route + [node])

    _backtrack(0, [])

    return optValue, optRoute
