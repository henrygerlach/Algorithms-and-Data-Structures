# Algorithms and Data Structures

A Python playground for implementing classic data structures and algorithms, including graph algorithms, sorting methods, and lossless compression.

## What is included

- `data_structures`: `Graph`, `Node`, `Edge`, `Queue`, `Stack`, `MinHeap`, `MaxHeap`, `UnionFind`, `BinaryTree`
- `sorting_algorithms`: `quick_sort`, `merge_sort`, `heap_sort`
- `graph_algorithms (shortest path and traversal)`: `bfs`, `dfs`, `dijkstra`, `floyd_warshall`
- `graph_algorithms (minimum spanning tree)`: `kruskal`
- `graph_algorithms (traveling salesperson)`: brute force and MST-based approaches
- `lossless_compression`: `lz78`, `huffman_coding`, and `lz78_huffman`
- notebooks: `examples.ipynb`, `testing.ipynb`

## Requirements

- Python 3.10+
- `numpy`
- `bitarray`

## Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy bitarray
```

## Project layout

```text
data_structures/
graph_algorithms/
helpers/
lossless_compression/
sorting_algorithms/
examples.ipynb
testing.ipynb
```

## Notes

- Example text files for compression live in `lossless_compression/data/`.
- Several modules are also re-exported via package `__init__.py` files for shorter imports.