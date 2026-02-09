from typing import List


class Queue:

    def __init__(
        self,
        queue: List,
    ):
        self.queue = queue
        self.size = len(queue)

    def insert(self, x):
        self.queue.append(x)
        self.size += 1
    
    def pop(self):
        out = self.queue.pop(0)
        self.size -= 1
        return out