from web3.contract import Contract
from functools import partial
from eth_utils import function_abi_to_4byte_selector, encode_hex

import copy

class IntentAction(object):
    def __init__(self, function):
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
        for attr, value in instance.__dict__.items():
            setattr(self, attr, value)

        data = encode_hex(function_abi_to_4byte_selector(self.abi))

        action = copy.copy(self)

        # TODO: Read output
        # self.abi['outputs'] = [{'name': '', 'type': self.function(instance, args)}]

        action.encoded = Contract._encode_abi(self.abi, args, data).decode()
        action.arguments = dict(zip([arg['name'] for arg in self.abi['inputs']], args))

        action.value = 0

        return action

    def __repr__(self):
        return str(self.abi)
