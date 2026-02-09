import sys
sys.path.append('..')

from data_structures import *

V1 = [Node(i) for i in range(6)]
E1 = [Edge(V1[start], V1[end], weight) for start, end, weight in [(0,1,1), (0,3,3), (1,3,5), (1,2,6), (1,4,1), (2,5,2), (2,4,5), (3,4,1), (4,5,4)]]
G1 = Graph(V1, E1, bidirectional=False)

V2 = [Node(i) for i in range(4)]
E2 = [Edge(V2[start], V2[end]) for start, end in [(0,1), (1,2), (2,3), (3,0)]]
G2 = Graph(V2, E2, bidirectional=True)
