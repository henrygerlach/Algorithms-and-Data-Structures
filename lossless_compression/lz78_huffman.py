import math
from typing import List, Tuple

from bitarray import bitarray

import lossless_compression.lz78 as lz78
import lossless_compression.huffman_coding as huffman_coding

from helpers.bitarray_helpers import bitarray_to_char, bitarray_to_int


def compress(
    data: str = None,
    max_dict_size: int = lz78.MAX_DICT_SIZE,
    from_file: str = None, 
    to_file: str = None,
    print_statistics: bool = False,
    return_output: bool = False
) -> bitarray:
    """
    Compress data using LZ78 + Huffman compression.
    
    :param data: Description of the data to compress
    :param from_file: Path to a file to read data from
    :param to_file: Path to a file to write compressed data to
    :param print_statistics: Whether to print compression statistics
    :param return_output: Whether to return the compressed data
    :return: Compressed data as a bitarray
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")
    
    if max_dict_size > lz78.MAX_DICT_SIZE:
        raise ValueError(f"max_dict_size cannot exceed {lz78.MAX_DICT_SIZE}")

    if from_file:
        with open(from_file, 'r') as f:
            data = f.read()

    # LZ78 Compression Algorithm
    lz78_compressed = lz78.compress(
        data=data,
        max_dict_size=max_dict_size,
        print_statistics=False,
        return_output=True
    )

    # Huffman Compression Algorithm
    huffman_compressed = huffman_coding.compress(
        data=data,
        print_statistics=False,
        return_output=True
    )

    lz78_huffman_compressed = huffman_coding.compress(
        data=lz78_to_str(deserialize_lz78(lz78_compressed)),
        print_statistics=False,
        return_output=True
    )

    if print_statistics:
        compute_statistics(
            original_data_size=len(data) * 8,
            lz78_compressed_size=len(lz78_compressed),
            huffman_compressed_size=len(huffman_compressed),
            lz78_huffman_compressed_size=len(lz78_huffman_compressed),
        )

    if to_file:
        with open(to_file, 'wb') as f:
            lz78_huffman_compressed.tofile(f)
    
    if return_output:
        return lz78_huffman_compressed

##### Helper Functions #####

def deserialize_lz78(compressed: bitarray) -> List[Tuple[int, str]]:
    pos = 0

    max_dict_size = bitarray_to_int(compressed[pos:pos + lz78.HEADER_SIZE])
    index_bits = math.ceil(math.log(max_dict_size + 1, 2)) 
    pos += lz78.HEADER_SIZE

    lz78_list = []
    while pos < len(compressed):
        idx = bitarray_to_int(compressed[pos:pos + index_bits])
        pos += index_bits
        ch = bitarray_to_char(compressed[pos:pos + 8])
        pos += 8
        lz78_list.append((idx, ch))
    
    return lz78_list

def lz78_to_str(lz78_list: List[Tuple[int, str]]) -> str:
    lz78_str = ""

    for idx, ch in lz78_list:
        lz78_str += f"{idx}{ch}"
    
    return lz78_str

def compute_statistics(
    original_data_size: str,
    lz78_compressed_size: int,
    huffman_compressed_size: int,
    lz78_huffman_compressed_size: int,
    return_output: bool = False,
) -> dict:
    compression_ratio = original_data_size / lz78_huffman_compressed_size
    improvement_over_lz78 = ((lz78_compressed_size - 
                              lz78_huffman_compressed_size) 
                              / lz78_compressed_size) * 100
    improvement_over_huffman = ((huffman_compressed_size - 
                                 lz78_huffman_compressed_size) 
                                 / huffman_compressed_size) * 100

    # add improvement over individual methods
    print("##### LZ78 + Huffman Compression Statistics #####")
    print(f"Original Size (bits):{original_data_size}")
    print(f"Only LZ78 Compressed Size (bits): {lz78_compressed_size}")
    print(f"Only Huffman Compressed Size (bits): {huffman_compressed_size}")
    print(f"LZ78 + Huffman Compressed Size (bits): "
          f"{lz78_huffman_compressed_size}\n\tImprovement over LZ78 (%): "
          f"{improvement_over_lz78:.2f}%\n\tImprovement over Huffman (%): "
          f"{improvement_over_huffman:.2f}%")
    print(f"Compression Ratio: {compression_ratio:.2f}")

    if return_output:
        return {
            "original_size_bits": original_data_size,
            "lz78_compressed_size_bits": lz78_compressed_size,
            "huffman_compressed_size_bits": huffman_compressed_size,
            "lz78_huffman_compressed_size_bits": lz78_huffman_compressed_size,
            "improvement_over_lz78_percent": improvement_over_lz78,
            "improvement_over_huffman_percent": improvement_over_huffman,
            "compression_ratio": compression_ratio,
        }
    
##### DECOMPRESSION METHODS #####

def decompress(
    data: bitarray = None, 
    to_file: str = None, 
    from_file: str = None, 
    return_output: bool = False
) -> str:
    """
    Decompress data using LZ78 + Huffman decompression.
    
    :param data: Compressed data as a bitarray
    :param from_file: Path to a file to read compressed data from
    :param to_file: Path to a file to write decompressed data to
    :param return_output: Whether to return the decompressed data
    :return: Decompressed data as a string
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")
    
    if from_file:
        with open(from_file, 'rb') as f:
            data = bitarray()
            data.fromfile(f)

    # Huffman Decompression Algorithm
    huffman_decompressed = huffman_coding.decompress(
        data=data,
        return_output=True
    )

    # LZ78 Decompression Algorithm
    lz78_decompressed = lz78.decompress(
        data=str_to_lz78(huffman_decompressed),
        return_output=True
    )

    if to_file:
        with open(to_file, 'w') as f:
            f.write(lz78_decompressed)
    
    if return_output:
        return lz78_decompressed
    
##### Helper Functions #####

def str_to_lz78(lz78_str: str) -> List[Tuple[int, str]]:
    lz78_list = []
    i = 0
    while i < len(lz78_str):
        idx_str = ""
        while i < len(lz78_str) and lz78_str[i].isdigit():
            idx_str += lz78_str[i]
            i += 1
        idx = int(idx_str) if idx_str else 0
        ch = lz78_str[i] if i < len(lz78_str) else ''
        lz78_list.append((idx, ch))
        i += 1
    return lz78_list