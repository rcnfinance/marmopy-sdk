from eth_utils import function_abi_to_4byte_selector, encode_hex
from web3.contract import Contract as ContractWeb3
import json


class Contract(object):

    def __init__(self, abi):
        true = True
        false = False
        self.abi = json.loads(abi)
        self.data = {"": None}
        self._construct()

    def _construct(self):
        for interface in self.abi:
            if interface["type"] == "function":
                self.data[interface['name']] = interface
                function = lambda args=None, name=interface["name"]: self.encode(args, name)
                function.__doc__ = str(interface)
                self.__setattr__(interface["name"], function)

    def encode(self, args=None, name=""):
        encoded_abi = None
        arguments = self.get_data_from_input(self.data[name], args)
        data = encode_hex(function_abi_to_4byte_selector(self.data[name]))
        encoded_abi = ContractWeb3._encode_abi(self.data[name], arguments, data)
        return encoded_abi

    def get_data_from_input(self, abi, params):
        arguments = []
        for inp in abi["inputs"]:
            # todo validate type
            arguments.append(params[inp["name"]])
        return arguments
