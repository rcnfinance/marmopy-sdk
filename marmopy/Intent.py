from marmopy.utils import (
    keccak256,
    to_hex_string_no_prefix_zero_padded,
    remove_0x_prefix)
from eth_utils import is_address
from time import time


class Intent(object):

    MAX_GAS_PRICE = 9999999999

    MIN_GAS_PRICE = 0

    SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'

    BYTECODE_1 = "6080604052348015600f57600080fd5b50606780601d6000396000f3fe6080604052366000803760008036600073"

    BYTECODE_2 = "5af43d6000803e8015156036573d6000fd5b3d6000f3fea165627a7a7230582033b260661546dd9894b994173484da72335f9efc37248d27e6da483f15afc1350029"

    MARMO_FACTORY_ADDRESS = "1053deb5e0f1697289b8a1b11aa870f07a7fb221"

    MARMO_ADDRESS = "3618a379f2624f42c0a8c79aad8db9d24d6e0312"

    EXPIRATION = 15

    def __init__(
        self,
        intentAction,
        signer,
        wallet=None,
        dependencies=list(),
        salt=SALT,
        max_gas_price=MAX_GAS_PRICE,
        min_gas_limit=MIN_GAS_PRICE,
        expiration=int(time()) + 365 * 86400 # 1 year from now
    ):
        self.to = intentAction.contractAddress
        self.value = intentAction.value
        self.data = intentAction.encoded
        self.dependencies = dependencies
        self.signer = signer
        self.wallet = wallet if wallet else self._generate_wallet_address(self.signer)
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.expiration = expiration,
        self.id = self._generate_id()

        assert(is_address(self.signer))
        assert(is_address(self.wallet))
        assert(is_address(self.to))

    def __repr__(self):
        return str(self.get_repr())

    def _generate_id(self):
        encoded_packed_builder = []
        encoded_packed_builder.append(self.wallet)
        dependencies = "".join(map(remove_0x_prefix, self.dependencies))
        encoded_packed_builder.append(keccak256(dependencies))
        encoded_packed_builder.append(remove_0x_prefix(self.to))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.value))
        encoded_packed_builder.append(keccak256(self.data))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.min_gas_limit))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.max_gas_price))
        encoded_packed_builder.append(remove_0x_prefix(self.salt))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.expiration))
        encoded_packed_builder = "".join(encoded_packed_builder)

        return "0x" + keccak256(encoded_packed_builder)

    def _generate_wallet_address(self, signer):
        signer = signer.replace("0x", "")
        init_code = keccak256(Intent.BYTECODE_1 + Intent.MARMO_ADDRESS + Intent.BYTECODE_2)
        concat = "ff" + Intent.MARMO_FACTORY_ADDRESS + "000000000000000000000000" + signer + init_code
        address = keccak256(concat)
        return "0x" + address[24:]

    def sign(self, credentials):
        results = self.get_repr()
        results["tx"] = {}
        for tx_key in ["to", "value", "data", "minGasLimit", "maxGasPrice"]:
            results["tx"][tx_key] = results.pop(tx_key)

        results["signature"] = credentials.sign_hash(self.id)
        return results

    def get_repr(self):
        data = {
            "to": self.to,
            "value": self.value,
            "data": self.data,
            "dependencies": self.dependencies,
            "signer": self.signer,
            "wallet": self.wallet,
            "salt": self.salt,
            "max_gas_price": self.max_gas_price,
            "min_gas_limit": self.min_gas_limit,
            "expiration": self.expiration,
            "id": self._generate_id()
        }
        return data
