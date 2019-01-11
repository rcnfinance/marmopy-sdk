
from eth_utils import (
    big_endian_to_int,
    remove_0x_prefix,
    to_checksum_address
)

from coincurve.keys import PrivateKey
from Crypto.Hash import keccak

def keccak256(hexstring):
    hexstring = remove_0x_prefix(hexstring)
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bytearray.fromhex(hexstring))
    return keccak_hash.hexdigest()

def to_hex_string_no_prefix_zero_padded(value, size=64):
    hexstring = hex(value).replace("0x", "")
    padding_size = 64 - len(hexstring)
    return "0" * padding_size + hexstring
