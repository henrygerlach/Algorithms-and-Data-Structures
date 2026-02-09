from typing import List


class Stack:

    def __init__(
        self,
        stack: List,
    ):
        self.stack = stack
        self.size = len(stack)

    def add(self, x):
        self.stack.append(x)
        self.size += 1
    
    def pop(self):
        out = self.stack.pop()
        self.size -= 1
        return out