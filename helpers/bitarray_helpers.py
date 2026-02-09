import struct

from bitarray import bitarray


DEFAULT_CHAR_BITS = 8
DEFAULT_FLOAT_BITS = 32
DEFAULT_VALUE_BITS = 32

DEFAULT_ENCODING = 'utf-8'


# int to bitarray
def int_to_bitarray(val: int, num_bits: int = DEFAULT_VALUE_BITS) -> bitarray:
    return bitarray(format(val, 'b').zfill(num_bits))

# bitarray to int
def bitarray_to_int(bit_arr: bitarray) -> int:
    return int(bit_arr.to01(), 2)

# float to bitarray
def float_to_bitarray(val: float) -> bitarray:
    bit_arr = bitarray()
    bit_arr.frombytes(struct.pack('f', val))
    return bit_arr

# bitarray to float
def bitarray_to_float(bit_arr: bitarray) -> float:
    byte_data = bit_arr.tobytes()
    return struct.unpack('f', byte_data)[0]

# char to bitarray
def char_to_bitarray(val: str) -> bitarray:
    bit_arr = bitarray()
    bit_arr.frombytes(val.encode(DEFAULT_ENCODING))
    return bit_arr

# bitarray to char
def bitarray_to_char(bit_arr: bitarray) -> str:
    byte_data = bit_arr.tobytes()
    return byte_data.decode(DEFAULT_ENCODING)