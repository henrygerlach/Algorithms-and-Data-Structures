from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Node:
    val: any
