import copy

from typing import Tuple

from data_structures import UnionFind, Graph


def kruskal(graph: Graph) -> Tuple[float, Graph]:
    mst = Graph(nodes=copy.deepcopy(graph.nodes), edges=[])
    mst_weight = 0
    num_mst_edges = 0

    graph.edges.sort(key=lambda x: x.weight)

    union_find = UnionFind(copy.deepcopy(graph.nodes))
    union_find.make_sets()

    ##### KRUSKAL ALGORITHM #####

    for edge in graph.edges:

        if num_mst_edges >= graph.V - 1:
            break

        posU = union_find.find(edge.start)
        posV = union_find.find(edge.end)

        if posU != posV:
            mst.edges.append(edge)
            mst_weight += edge.weight
            num_mst_edges += 1
            union_find.union(posU, posV)

    return mst_weight, mst