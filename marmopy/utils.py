
from eth_utils import (
    big_endian_to_int,
    remove_0x_prefix,
    to_checksum_address,
    to_normalized_address
)

from coincurve.keys import PrivateKey
from Crypto.Hash import keccak

import sys

def keccak256(hexstring):
    hexstring = remove_0x_prefix(hexstring)
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bytearray.fromhex(hexstring))
    return keccak_hash.hexdigest()

def to_hex_string_no_prefix_zero_padded(value, size=64):
    hexstring = hex(value).replace("0x", "").replace('L', '')
    padding_size = 64 - len(hexstring)
    return "0" * padding_size + hexstring

def to_padded(val, size=64):
    val = val.replace("0x", "")
    return "0" * (size - len(val)) + val

def to_bytes_32(val):
    val = val.replace("0x", "")
    return val + "0" * (64 - len(val))

def to_bytes(s):
    if (sys.version_info > (3, 0)):
        return bytes.fromhex(s.replace('0x', ''))
    else:
        return s.replace('0x', '').decode('hex')

def from_bytes(b):
    if (sys.version_info > (3, 0)):
        return '0x' + b.hex()
    else:
        return '0x' + b.encode('hex')

def decode_receipt_event(data):
    data = to_bytes(data)

    # Fixed position parameters
    success = big_endian_to_int(data[:32]) != 0
    result_start = big_endian_to_int(data[32:64])
    result_size = big_endian_to_int(data[result_start:result_start + 32])

    # Dynamic position parameters
    result = from_bytes(data[result_start + 32:result_start + 32 +result_size])

    return {
        "success": success,
        "result": result
    }
