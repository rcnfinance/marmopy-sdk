from web3.contract import Contract
from functools import partial
from eth_utils import function_abi_to_4byte_selector, encode_hex

class Action(object):
    def __init__(self, function):
        if isinstance(function, dict):
            if function['payable']:
                self.value_name = "_payable"
                self.value_offset = len(function['inputs'])
            else:
                self.value_name = None
                self.value_offset = None

            self.abi = function
        else:
            self.abi = {}

            self.function = function
            self.abi['name'] = function.__name__

            args_names = [var for var in function.__code__.co_varnames if var != "self"]
            args_types = function.__defaults__ if len(args_names) > 0 else []

            if len(args_names) != len(args_types):
                raise TypeError("Missing Argument Types")

            if args_types.count("payable") > 1:
                raise TypeError("Multiple payable types are not allowed")

            try:
                self.value_offset = args_types.index("payable")
                self.value_name = args_names[self.value_offset]
                args_names = tuple(x for x in args_names if x != self.value_name)
                args_types = tuple(x for x in args_types if x != "payable")
            except ValueError:
                self.value_offset = None
                self.value_name = None

            self.abi['inputs'] = [{"name": arg, "type": arg_type} for arg, arg_type in zip(args_names, args_types)]
            self.abi['type'] = "function"

    def __get__(self, instance, obj):
        """Support instance methods."""
        return partial(self.__call__, instance)

    def __call__(self, instance, *args, **kwargs):
        selector = encode_hex(function_abi_to_4byte_selector(self.abi))

        # TODO: Read output
        # self.abi['outputs'] = [{'name': '', 'type': self.function(instance, args)}]
        value = 0

        if len(args) != 0 and isinstance(args[0], dict):
            if self.value_offset != None:
                value = self.args[0][self.value_name]

            params = self.order_dict_args(args[0], self.value_name)
        else:
            if self.value_offset != None:
                value = args[self.value_offset]
                args = args[:self.value_offset] + args[self.value_offset + 1:]

            params = args

        return {
            "to": instance.address,
            "value": value,
            "data": Contract._encode_abi(self.abi, params, selector).decode()
        }

    def order_dict_args(self, args, exclude):
        result = []

        for i in self.abi["inputs"]:
            if i != exclude:
                result.append(args[i["name"]])

        return result

    def __repr__(self):
        return str(self.abi)
