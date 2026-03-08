import sys

from typing import List, Tuple


class MinHeap:
    def __init__(self, heap: List[Tuple[int, ...]]) -> None:
        self.size = len(heap)
        self.heap = self.build_heap(heap=heap)

    ##### Helpers #####

    def get_left_child(self, pos: int) -> int:
        return 2 * pos + 1

    def get_right_child(self, pos: int) -> int:
        return 2 * pos + 2

    def get_parent(self, pos: int) -> int:
        return abs(pos - 1) // 2

    def is_leaf(self, pos: int) -> bool:
        return (
            self.get_left_child(pos) >= self.size
            and self.get_right_child(pos) >= self.size
        )

    def swap(self, pos1: int, pos2: int) -> None:
        self.heap[pos1], self.heap[pos2] = self.heap[pos2], self.heap[pos1]

    ##### MinHeap Methods #####

    def heapify(self, pos: int) -> None:
        smallest = sys.maxsize
        l = self.get_left_child(pos)
        r = self.get_right_child(pos)

        if l < self.size and self.heap[l][0] < self.heap[pos][0]:
            smallest = l
        else:
            smallest = pos

        if r < self.size and self.heap[r][0] < self.heap[smallest][0]:
            smallest = r

        if smallest != pos:
            self.swap(smallest, pos)
            self.heapify(smallest)

    def build_heap(self, heap: List[int] = None) -> List[int]:
        if heap:
            self.heap = heap

        for i in range((len(self.heap) // 2), -1, -1):
            self.heapify(i)

        return self.heap

    def insert(self, ele: Tuple[int, ...]) -> None:
        self.heap.append(ele)
        self.size += 1

        current = self.size - 1
        while True:
            parent = self.get_parent(current)
            if self.heap[current][0] < self.heap[parent][0]:
                self.swap(current, parent)
                current = parent
            else:
                break

    def get_min(self) -> Tuple[int, ...]:
        min_tuple = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        del self.heap[self.size - 1]
        self.size -= 1
        self.heapify(0)
        return min_tuple

    def decrease_key(
        self, new_prio: int, key: Tuple[int, ...] = None, pos: int = None
    ) -> None:
        if key:
            pos = self.get_index(key)
        self.heap[pos] = (new_prio, *self.heap[pos][1:])

        current = pos
        while True:
            parent = self.get_parent(current)
            if self.heap[current][0] < self.heap[parent][0]:
                self.swap(current, parent)
                current = parent
            else:
                break

    def get_index(self, key: Tuple[int, ...]) -> int:
        try:
            return self.heap.index(key)
        except ValueError:
            return None
