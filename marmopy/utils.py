from eth_utils.hexadecimal import *
from eth_hash.auto import keccak as keccak_256
from web3.auto import w3

class Credentials: 
    def __init__(self,privateKey):
        self._Account = w3.eth.account.privateKeyToAccount(privateKey)
        
    def getAddress(self):
        return self._Account.address

    def signHash(self,hashstring):
        signature = dict(self._Account.signHash(hashstring))
  
        for key in tuple(signature.keys()):
            if key in ["r","s","v"]:
                signature[key] = hex(signature[key])
            else:
                signature.pop(key)
        return signature
    
def keccak256(hexstring: str):
    return keccak_256(bytearray.fromhex(remove_0x_prefix(hexstring))).hex()

def toHexStringNoPrefixZeroPadded(value,size=64):
    hexstring = hex(value).replace("0x","")
    padding_size = 64 - len(hexstring)
    return "0"*padding_size + hexstring