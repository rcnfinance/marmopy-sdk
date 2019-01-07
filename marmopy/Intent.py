from marmopy.utils import (
    keccak256,
    toHexStringNoPrefixZeroPadded,
    remove_0x_prefix)
from eth_utils import is_address


class Intent:
    MAX_GAS_PRICE = 9999999999
    MIN_GAS_PRICE = 0
    SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'

    def __init__(self, intent_action, signer, wallet, dependencies=list(),
                 salt=SALT, max_gas_price=MAX_GAS_PRICE, min_gas_limit=MIN_GAS_PRICE):

        self.to = intent_action.contractAddress
        self.value = intent_action.value
        self.data = intent_action.encoded
        self.dependencies = dependencies
        self.signer = signer
        self.wallet = wallet
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.id = self._generate_id()

        assert(is_address(self.signer))
        assert(is_address(self.wallet))
        assert(is_address(self.to))

    def __repr__(self):
        return str(self.__dict__)

    def _generate_id(self):
        encoded_packed_builder = []
        encoded_packed_builder.append(self.wallet)
        dependencies = "".join(map(remove_0x_prefix, self.dependencies))
        encoded_packed_builder.append(keccak256("0x" + dependencies if dependencies != "" else dependencies))
        encoded_packed_builder.append(remove_0x_prefix(self.to))
        encoded_packed_builder.append(toHexStringNoPrefixZeroPadded(self.value))
        encoded_packed_builder.append(keccak256(self.data))
        encoded_packed_builder.append(toHexStringNoPrefixZeroPadded(self.min_gas_limit))
        encoded_packed_builder.append(toHexStringNoPrefixZeroPadded(self.max_gas_price))
        encoded_packed_builder.append(remove_0x_prefix(self.salt))
        encoded_packed_builder = "".join(encoded_packed_builder)

        return "0x" + keccak256(encoded_packed_builder)

    def sign(self, credentials):
        results = self.__dict__.copy()
        results["tx"] = {}
        for tx_key in ["to", "value", "data", "min_gas_limit", "max_gas_price"]:
            results["tx"][tx_key] = results.pop(tx_key)

        results["signature"] = credentials.signHash(self.id)

        return results


class IntentGeneric(Intent):
    def __init__(self, data, contract_address, value, signer, wallet, dependencies=list(),
                 salt=Intent.SALT, max_gas_price=Intent.MAX_GAS_PRICE, min_gas_limit=Intent.MIN_GAS_PRICE):
        self.to = contract_address
        self.value = value
        self.data = data
        self.dependencies = dependencies
        self.signer = signer
        self.wallet = wallet
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.id = self._generateId()

        assert(is_address(self.signer))
        assert(is_address(self.wallet))
        assert(is_address(self.to))
