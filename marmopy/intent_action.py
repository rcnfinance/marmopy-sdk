from web3.contract import Contract
from functools import partial
from eth_utils import function_abi_to_4byte_selector, encode_hex

class Action(object):
    def __init__(self, function):
        if isinstance(function, dict):
            self.abi = function
        else:
            self.abi = {}

            self.function = function
            self.abi['name'] = function.__name__

            args_names = [var for var in function.__code__.co_varnames if var != "self"]
            args_types = function.__defaults__ if len(args_names) > 0 else []

            if len(args_names) != len(args_types):
                raise TypeError("Missing Argument Types")

            self.abi['inputs'] = [{"name": arg, "type": arg_type} for arg, arg_type in zip(args_names, args_types)]
            self.abi['type'] = "function"

    def __get__(self, instance, obj):
        """Support instance methods."""
        return partial(self.__call__, instance)

    def __call__(self, instance, *args, **kwargs):
        selector = encode_hex(function_abi_to_4byte_selector(self.abi))

        # TODO: Read output
        # self.abi['outputs'] = [{'name': '', 'type': self.function(instance, args)}]

        if len(args) != 0 and isinstance(args[0], dict):
            params = self.order_dict_args(args[0])
        else:
            params = args

        return {
            "to": instance.address,
            "value": 0,
            "data": Contract._encode_abi(self.abi, params, selector).decode()
        }

    def order_dict_args(self, args):
        result = []

        for i in self.abi["inputs"]:
            result.append(args[i["name"]])

        return result

    def __repr__(self):
        return str(self.abi)
