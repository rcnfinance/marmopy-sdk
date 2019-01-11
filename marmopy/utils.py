
from eth_utils import (
    big_endian_to_int,
    remove_0x_prefix,
    to_checksum_address)
from coincurve.keys import PrivateKey
from Crypto.Hash import keccak


class Credentials:
    def __init__(self, private_key):
        self.private_key = PrivateKey(bytes(bytearray.fromhex(private_key)))

    def get_address(self):
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(self.private_key.public_key.format(compressed=False,)[1:])
        return to_checksum_address(keccak_hash.digest()[-20:])

    def sign_hash(self, hashstring):
        msg_hash = bytes(bytearray.fromhex(remove_0x_prefix(hashstring)))

        signature_bytes = self.private_key.sign_recoverable(msg_hash, hasher=None)

        assert len(signature_bytes) == 65

        r = "0x" + format(big_endian_to_int(signature_bytes[0:32]), "x")

        s = "0x" + format(big_endian_to_int(signature_bytes[32:64]), "x")

        v = hex(ord(signature_bytes[64:65]) + 27)

        return {"r": r, "s": s, "v": v}


def keccak256(hexstring):
    hexstring = remove_0x_prefix(hexstring)
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bytearray.fromhex(hexstring))
    return keccak_hash.hexdigest()


def to_hex_string_no_prefix_zero_padded(value, size=64):
    hexstring = hex(value).replace("0x", "")
    padding_size = 64 - len(hexstring)
    return "0" * padding_size + hexstring
