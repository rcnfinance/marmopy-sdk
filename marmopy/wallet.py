
from eth_utils import (
    big_endian_to_int,
    remove_0x_prefix,
    to_checksum_address
)

from coincurve.keys import PrivateKey
from Crypto.Hash import keccak
from .intent import Intent, SignedIntent
from .utils import keccak256
from .config import Config

class Credentials:
    def __init__(self, private_key):
        if private_key.startswith("0x"):
            private_key = private_key[2:]

        self.private_key = PrivateKey(bytes(bytearray.fromhex(private_key)))

    @property
    def address(self):
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(self.private_key.public_key.format(compressed=False,)[1:])
        return to_checksum_address(keccak_hash.digest()[-20:])

    def sign(self, message):
        msg_hash = bytes(bytearray.fromhex(remove_0x_prefix(message)))

        signature_bytes = self.private_key.sign_recoverable(msg_hash, hasher=None)

        assert len(signature_bytes) == 65

        r = "0x" + format(big_endian_to_int(signature_bytes[0:32]), "x")
        s = "0x" + format(big_endian_to_int(signature_bytes[32:64]), "x")
        v = hex(ord(signature_bytes[64:65]) + 27)

        return {"r": r, "s": s, "v": v}

class Wallet:
    def __init__(self, private_key):
        if Config.configured is False:
            raise AssertionError("MarmoPY Should be configured or a custom configuration should be provided")
            
        if isinstance(private_key, Credentials):
            self.credentials = private_key
        else:
            self.credentials = Credentials(private_key)

        self.config = Config

        self.signer = self.credentials.address
    

    @property
    def address(self):
        signer = remove_0x_prefix(self.signer)
        concat = "ff" + remove_0x_prefix(self.config.factory) + "000000000000000000000000" + signer + remove_0x_prefix(self.config.init_code)
        address = keccak256(concat)
        return "0x" + address[24:]

    def sign(self, intent):
        # if intent is not Intent:
        #     raise ValueError("Object to sign should be an intent")
        
        return SignedIntent(intent, self, self.credentials.sign(intent.id(self)))
