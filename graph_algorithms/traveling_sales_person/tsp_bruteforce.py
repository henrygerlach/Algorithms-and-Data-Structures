from typing import Tuple, List

from data_structures import Graph


def tsp_bruteforce(graph: Graph) -> Tuple[float, List[int]]:
    opt_route = []
    opt_value = float("inf")

    def _backtrack(k: int, route: List[int]):
        nonlocal opt_value
        nonlocal opt_route

        if k == graph.V:
            cur_value = sum(
                graph.get_distance(route[i], route[i + 1]) for i in range(k - 1)
            ) + graph.get_distance(route[k - 1], route[0])
            if cur_value < opt_value:
                opt_value = cur_value
                opt_route = route
        else:
            for node in list(set(graph.nodes).difference(set(route))):
                _backtrack(k + 1, route + [node])

    _backtrack(0, [])

    return opt_value, opt_route
