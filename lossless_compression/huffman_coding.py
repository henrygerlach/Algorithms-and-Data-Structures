from helpers import bitarray_to_int, int_to_bitarray
from data_structures import Node, Queue, BinaryTree

from bitarray import bitarray


NUM_BITS_FOR_TREE_SIZE = 16  # using 16 bits to store tree size allows for
# trees up to 65535 bits


##### COMPRESSION METHODS #####


def compress(
    data: str = None,
    from_file: str = None,
    to_file: str = None,
    print_statistics: bool = False,
    return_output: bool = False,
) -> bitarray:
    """
    Compress data using Huffman coding.

    :param data: Description of the data to compress
    :param from_file: Path to a file to read data from
    :param to_file: Path to a file to write compressed data to
    :param print_statistics: Whether to print compression statistics
    :param return_output: Whether to return the compressed data
    :return: Compressed data as a bitarray
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")

    if from_file:
        with open(from_file, "r") as f:
            data = f.read()

    binary_tree = _compute_binary_tree(data)
    binary_codes = _compute_binary_codes(binary_tree)

    compressed_data = bitarray("".join(binary_codes[char] for char in data))
    serialized_tree = binary_tree.serialize(
        val_type="char", val_func=lambda x: x[0], only_leaf_vals=True
    )

    # first NUM_BITS_FOR_TREE_SIZE bits indicate length of serialized tree,
    # followed by tree and compressed data
    compressed = (
        int_to_bitarray(len(serialized_tree), NUM_BITS_FOR_TREE_SIZE)
        + serialized_tree
        + compressed_data
    )

    if print_statistics:
        compute_statistics(
            data=data,
            serialized_tree_size=len(serialized_tree),
            compressed_data_size=len(compressed_data),
            print_output=True,
            return_output=False,
        )

    if to_file:
        with open(to_file, "wb") as f:
            compressed.tofile(f)

    if return_output:
        return compressed


def _compute_binary_tree(data: str) -> BinaryTree:
    # Compute character occurrence frequencies
    data_size = len(data)
    sorted_frequencies = dict(
        sorted(
            {char: data.count(char) / data_size for char in set(data)}.items(),
            key=lambda item: item[1],
        )
    )

    # Build Huffman tree using two-queue method
    q1 = Queue(
        [BinaryTree(Node((ch, freq))) for ch, freq in sorted_frequencies.items()]
    )
    q2 = Queue([])

    while q1.size + q2.size > 1:
        trees = []
        new_freq = 0.0
        for _ in range(2):
            if not q1.size:
                trees.append(q2.pop())
                new_freq += trees[-1].root.val
            elif not q2.size:
                trees.append(q1.pop())
                new_freq += trees[-1].root.val[1]
            else:
                if q1.queue[0].root.val[1] > q2.queue[0].root.val:
                    trees.append(q2.pop())
                    new_freq += trees[-1].root.val
                else:
                    trees.append(q1.pop())
                    new_freq += trees[-1].root.val[1]

        q2.insert(BinaryTree(Node(new_freq), left=trees[0], right=trees[1]))

    return q2.queue[0]


def _compute_binary_codes(binary_tree: BinaryTree) -> dict:
    binary_codes = {}

    # Traverse the binary tree to assign binary codes to characters
    # using '0' for left and '1' for right
    def _traverse_tree(node: BinaryTree, code: str):
        if node.is_leaf():
            binary_codes[node.root.val[0]] = code
            return

        if node.left:
            _traverse_tree(node.left, code + "0")
        if node.right:
            _traverse_tree(node.right, code + "1")

    _traverse_tree(binary_tree, "")
    return binary_codes


def compute_statistics(
    data: str,
    serialized_tree_size: int,
    compressed_data_size: int,
    header_size: int = NUM_BITS_FOR_TREE_SIZE,
    print_output: bool = False,
    return_output: bool = True,
) -> dict:
    original_size_bits = len(data) * 8
    total_size_bits = compressed_data_size + serialized_tree_size + header_size

    compression_ratio = original_size_bits / total_size_bits

    if print_output:
        print("##### Huffman Compression Statistics #####")
        print(f"Original Size (bits): {original_size_bits}")
        print(f"Compressed Size (bits): {compressed_data_size}")
        print(f"Serialized Tree Size (bits): {serialized_tree_size}")
        print(f"Total Compressed Size (bits): {total_size_bits}")
        print(f"Compression Ratio: {compression_ratio:.2f}")

    if return_output:
        return {
            "original_size_bits": original_size_bits,
            "compressed_data_size_bits": compressed_data_size,
            "serialized_tree_size_bits": serialized_tree_size,
            "total_size_bits": total_size_bits,
            "compression_ratio": compression_ratio,
        }


##### DECOMPRESSION METHODS #####


def decompress(
    data: bitarray = None,
    to_file: str = None,
    from_file: str = None,
    return_output: bool = False,
) -> str:
    """
    Decompress data using Huffman coding.

    :param data: Compressed data as a bitarray
    :param to_file: Path to a file to write decompressed data to
    :param from_file: Path to a file to read compressed data from
    :param return_output: Whether to return the decompressed data
    :return: Decompressed data as a string
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")

    if from_file:
        with open(from_file, "rb") as f:
            data = bitarray()
            data.fromfile(f)

    # first NUM_BITS_FOR_TREE_SIZE bits indicate length of serialized tree
    # followed by tree and compressed data
    bits_for_tree_size = NUM_BITS_FOR_TREE_SIZE
    tree_size = bitarray_to_int(data[:bits_for_tree_size])
    serialized_tree = data[bits_for_tree_size : bits_for_tree_size + tree_size]
    compressed_data = data[bits_for_tree_size + tree_size :]

    binary_tree = BinaryTree.deserialize(
        serialized_tree, val_type="char", only_leaf_vals=True
    )

    # Decompress data using the binary tree, traversing left
    # for '0' and right for '1'
    result = []
    cur_node = binary_tree
    for bit in compressed_data:
        if bit == 0:
            cur_node = cur_node.left
        else:
            cur_node = cur_node.right

        if cur_node.is_leaf():
            result.append(cur_node.root.val[0])
            cur_node = binary_tree
    out = "".join(result)

    if to_file:
        with open(to_file, "w") as f:
            f.write(out)

    if return_output:
        return out
