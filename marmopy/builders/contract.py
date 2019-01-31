from eth_utils import function_abi_to_4byte_selector, encode_hex
from web3.contract import Contract as ContractWeb3
from marmopy import Action

import hashlib
import json

def __generic_contract_init__(self, address):
    self.address = address

class Contract(object):
    def __new__(self, abi):
        methods = {
            "__init__": __generic_contract_init__
        }

        for interface in json.loads(abi):
            if interface["type"] == "function":
                methods[interface["name"]] = Action(interface)
        
        return type(
            "GenericContract-" + hashlib.sha1(abi.encode('utf-8')).hexdigest()[:8], (), methods
        )
