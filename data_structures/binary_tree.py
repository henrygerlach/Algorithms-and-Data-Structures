from .node import Node
from .queue import Queue
from helpers.bitarray_helpers import (
    DEFAULT_CHAR_BITS,
    DEFAULT_FLOAT_BITS,
    DEFAULT_VALUE_BITS,
    bitarray_to_char,
    bitarray_to_float,
    bitarray_to_int,
    char_to_bitarray,
    float_to_bitarray,
    int_to_bitarray,
)

from typing import Tuple
from bitarray import bitarray


class BinaryTree:
    def __init__(
        self,
        root: Node,
        left: "BinaryTree" = None,
        right: "BinaryTree" = None,
    ) -> None:
        self.root = root
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls: "BinaryTree", vals: list) -> "BinaryTree":
        """
        Create a binary tree from a list representation
        (level-order traversal).

        :param cls: Class reference
        :param vals: List of values (use None for missing nodes)
        :return: Binary tree constructed from the list
        """
        if not vals:
            return None

        def _helper(index: int) -> Tuple["BinaryTree", int]:
            if index >= len(vals) or vals[index] is None:
                return None, index + 1

            node = Node(vals[index])
            left_subtree, next_index = _helper(index + 1)
            right_subtree, next_index = _helper(next_index)

            return BinaryTree(node, left_subtree, right_subtree), next_index

        tree, _ = _helper(0)
        return tree

    @classmethod
    def deserialize(
        cls: "BinaryTree",
        bit_arr: bitarray,
        val_type: str,
        val_bits: int = DEFAULT_VALUE_BITS,
        only_leaf_vals: bool = False,
    ) -> "BinaryTree":
        """
        Deserialize a binary tree from a bitarray representation.

        :param cls: Class reference
        :param bit_arr: Bitarray representation of the tree
        :param val_type: Type of values stored in the tree nodes
        :param val_bytes: Number of bytes used to represent each value
        :param only_leaf_vals: Whether only leaf nodes carry values
        :return: Deserialized binary tree
        """

        def _decode(index: int) -> Tuple["BinaryTree", int]:
            # if bit is 0, Node not present or end of array
            if index >= len(bit_arr) or bit_arr[index] == 0:
                return None, index + 1 if only_leaf_vals else index + 2
            index += 1

            # if only_leaf_vals, next bit encodes whether this node is a leaf
            is_leaf = False
            if only_leaf_vals:
                is_leaf = bit_arr[index] == 1
                index += 1

            # only leaves carry values when only_leaf_vals is True
            val = 0 if val_type == "int" else 0.0 if val_type == "float" else ""
            if not only_leaf_vals or is_leaf:
                if val_type == "int":
                    val = bitarray_to_int(bit_arr[index : index + val_bits])
                    index += val_bits
                elif val_type == "float":
                    val = bitarray_to_float(bit_arr[index : index + DEFAULT_FLOAT_BITS])
                    index += DEFAULT_FLOAT_BITS
                elif val_type == "char":
                    val = bitarray_to_char(bit_arr[index : index + DEFAULT_CHAR_BITS])
                    index += DEFAULT_CHAR_BITS
                else:
                    raise ValueError("Unsupported value type")

            node = Node(val)

            # only traverse children for internal nodes
            left_subtree = right_subtree = None
            if not is_leaf:
                left_subtree, index = _decode(index)
                right_subtree, index = _decode(index)

            return BinaryTree(node, left_subtree, right_subtree), index

        tree, _ = _decode(0)
        return tree

    def serialize(
        self,
        val_type: str,
        val_bits: int = DEFAULT_VALUE_BITS,
        val_func: callable = None,
        only_leaf_vals: bool = False,
    ) -> bitarray:
        """
        Docstring für serialize

        :param self: Instance of BinaryTree
        :param val_type: Type of values stored in the tree nodes
        :param val_bytes: Number of bytes used to represent each value
        :param val_func: Function to apply to each value before serialization
        :param only_leaf_vals: Whether only leaf nodes should be serialized
        with values
        :return: Bitarray representation of the serialized tree
        """
        bit_arr = bitarray()

        def _serialize(
            cur: "BinaryTree",
        ) -> None:
            # 0 for Node not present, else 1 for present
            if not cur:
                bit_arr.append(0)
                return
            bit_arr.append(1)

            # Extra bit to mark leaf if only_leaf_vals
            # so deserializer knows where values live
            is_leaf = cur.is_leaf()
            if only_leaf_vals:
                bit_arr.append(1 if is_leaf else 0)

            # Only write values for leaves when only_leaf_vals is True
            # or for all nodes otherwise
            if not only_leaf_vals or is_leaf:
                # Apply function to value if provided
                val = cur.root.val
                if val_func:
                    val = val_func(val)

                # Serialize value based on type
                if val_type == "int":
                    bit_arr.extend(int_to_bitarray(val, val_bits))
                elif val_type == "float":
                    bit_arr.extend(float_to_bitarray(val))
                elif val_type == "char":
                    bit_arr.extend(char_to_bitarray(val))
                else:
                    raise ValueError("Unsupported value type")

            # Recurse on children only for internal nodes
            # when using leaf-only values
            if not is_leaf:
                _serialize(cur.left)
                _serialize(cur.right)

            return bit_arr

        _serialize(self)
        return bit_arr

    ##### Utility Methods #####

    def __str__(self) -> str:
        return f"BinaryTree(val={self.root},left={self.left}, \
            right={self.right})"

    def is_leaf(self) -> bool:
        return (not self.left) and (not self.right)

    def find(self, val):

        def _find(val: any, cur: "BinaryTree") -> "BinaryTree":
            if not cur:
                return None

            if cur.root.val == val:
                return cur

            left = _find(val, cur.left)
            if not left:
                return _find(val, cur.right)
            return left

        return _find(val, self)

    def print_tree(self):
        queue = Queue([(self, 0)])

        while queue.size:
            ele = queue.pop()
            if not ele[0]:
                continue
            layer = ele[1]
            print(f"Layer {layer}: {ele[0].root.val}")
            queue.insert((ele[0].left, layer + 1))
            queue.insert((ele[0].right, layer + 1))
