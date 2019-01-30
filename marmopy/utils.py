
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
    dependencies_start = big_endian_to_int(data[:32])
    relayer = to_normalized_address(data[32:64])
    value = big_endian_to_int(data[64:96])
    data_start = big_endian_to_int(data[96:128])
    salt = from_bytes(data[128:160])
    expiration = big_endian_to_int(data[160:192])
    success = big_endian_to_int(data[192:224]) != 0

    # Dynamic position parameters
    dependencies_size = big_endian_to_int(data[dependencies_start:dependencies_start + 32])
    dependencies = from_bytes(data[dependencies_start + 32:dependencies_start + 32 +dependencies_size])

    data_size = big_endian_to_int(data[data_start:data_start + 32])
    data = from_bytes(data[data_start + 32:data_start + 32 + data_size])

    return {
        "dependencies": dependencies,
        "relayer": relayer,
        "value": value,
        "data": data,
        "salt": salt,
        "expiration": expiration,
        "success": success
    }
