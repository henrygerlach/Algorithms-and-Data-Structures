from helpers.bitarray_helpers import bitarray_to_int, int_to_bitarray, char_to_bitarray, bitarray_to_char

import math

from bitarray import bitarray


DEFAULT_ENCODING_BITS = 8
MAX_DICT_SIZE = 2 ** 16 - 1
HEADER_SIZE = math.ceil(math.log(MAX_DICT_SIZE, 2))


##### COMPRESSION METHODS #####

def compress(
    data: str = None,
    max_dict_size: int = MAX_DICT_SIZE,
    from_file: str = None, 
    to_file: str = None,
    print_statistics: bool = False,
    return_output: bool = False
) -> bitarray:
    """
    Compress data using LZ78 compression.
    
    :param data: Description of the data to compress
    :param from_file: Path to a file to read data from
    :param to_file: Path to a file to write compressed data to
    :param print_statistics: Whether to print compression statistics
    :param return_output: Whether to return the compressed data
    :return: Compressed data as a bitarray
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")
    
    if max_dict_size > MAX_DICT_SIZE:
        raise ValueError(f"max_dict_size cannot exceed {MAX_DICT_SIZE}")
    index_bits = math.ceil(math.log(max_dict_size + 1, 2))

    if from_file:
        with open(from_file, 'r') as f:
            data = f.read()

    # LZ78 Compression Algorithm
    dict = []
    dict_size = 0
    payload = bitarray()

    prefix = ''
    for ch in data:
        new = prefix + ch

        if new in dict:
            prefix = new
        else:
            idx = 0 
            if prefix:
                idx = dict.index(prefix) + 1
            
            payload.extend(int_to_bitarray(idx, index_bits))
            payload.extend(char_to_bitarray(ch))

            if dict_size < MAX_DICT_SIZE:
                dict.append(new)
                dict_size += 1

            prefix = ''

    idx = 0 
    if prefix:
        idx = dict.index(prefix) + 1

    # End of Data Marker
    payload.extend(int_to_bitarray(idx, index_bits))
    payload.extend(char_to_bitarray(chr(0)))

    # Construct final output with header containing max_dict_size
    header = int_to_bitarray(max_dict_size, HEADER_SIZE)
    out = header + payload

    if print_statistics:
        compute_statistics(
            data=data,
            compressed=out,
            print_output=True,
            return_output=False
        )

    if to_file:
        with open(to_file, 'wb') as f:
            out.tofile(f)

    if return_output:
        return out

##### DECOMPRESSION METHODS #####

def decompress(
    data: bitarray = None,
    from_file: str = None,
    to_file: str = None,
    return_output: bool = False
) -> str:
    """
    Decompress data using LZ78 compression.
    
    :param data: Compressed data as a bitarray
    :param from_file: Path to a file to read compressed data from
    :param to_file: Path to a file to write decompressed data to
    :param print_statistics: Whether to print decompression statistics
    :param return_output: Whether to return the decompressed data
    :return: Decompressed data as a string
    """
    if not data and not from_file:
        raise ValueError("Either data or from_file must be provided")
    
    if from_file:
        with open(from_file, 'rb') as f:
            data = bitarray()
            data.fromfile(f)

    index = 0
    max_dict_size = bitarray_to_int(data[index:index + HEADER_SIZE])
    index += HEADER_SIZE

    index_bits = math.ceil(math.log(max_dict_size + 1, 2))
    
    # LZ78 Decompression Algorithm
    dict = []
    out = ''
    while index + index_bits + DEFAULT_ENCODING_BITS <= len(data):
        idx = bitarray_to_int(data[index:index + index_bits])
        index += index_bits

        ch = bitarray_to_char(data[index:index + DEFAULT_ENCODING_BITS])
        index += DEFAULT_ENCODING_BITS

        entry = ''
        if idx > 0:
            entry = dict[idx - 1]
        entry += ch

        out += entry

        if len(dict) < max_dict_size and entry:
            dict.append(entry)

    if to_file:
        with open(to_file, 'w') as f:
            f.write(out)

    if return_output:
        return out
    
##### HELPER METHODS #####

def compute_statistics(
    data: str, 
    compressed: bitarray, 
    print_output: bool = False, 
    return_output: bool = True
) -> dict:
    original_size_bits = len(data) * 8 
    compressed_size_bits = len(compressed)
    compression_ratio = original_size_bits / compressed_size_bits

    if print_output:
        print("##### LZ78 Compression Statistics #####")
        print(f"Original Size (bits): {original_size_bits}")
        print(f"Compressed Size (bits): {compressed_size_bits}")
        print(f"Compression Ratio: {compression_ratio:.2f}")

    if return_output:
        return {
            "original_size_bits": original_size_bits,
            "compressed_size_bits": compressed_size_bits,
            "compression_ratio": compression_ratio,
        }
