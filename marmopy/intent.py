import requests

from eth_utils import (
    remove_0x_prefix
)
from marmopy.utils import (
    keccak256,
    to_hex_string_no_prefix_zero_padded
)
from eth_utils import is_address
from time import time
from provider import global_provider
from constants import wallet_abi
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from status_receipt import IntentReceipt, StatusReceipt, Status
from utils import decode_receipt_event

import json

class Intent(object):
    DEFAULT_SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'
    DEFAULT_MIN_GAS_LIMIT = 0
    DEFAULT_MAX_GAS_PRICE = 9999999999

    def __init__(
        self,
        intent_action,
        dependencies=list(),
        salt = DEFAULT_SALT,
        max_gas_price = DEFAULT_MAX_GAS_PRICE,
        min_gas_limit = DEFAULT_MIN_GAS_LIMIT,
        expiration = int(time()) + 365 * 86400 # 1 year from now
    ):
        self.to = intent_action.contractAddress
        self.value = intent_action.value
        self.data = intent_action.encoded
        self.dependencies = dependencies
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.expiration = expiration

        assert(is_address(self.to))

    def id(self, wallet):
        encoded_packed_builder = []
        encoded_packed_builder.append(wallet.address)
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

class IntentGeneric(Intent):
    def __init__(
            self,
            data,
            contract_address,
            value,
            dependencies=list(),
            salt=Intent.DEFAULT_SALT,
            max_gas_price=Intent.DEFAULT_MAX_GAS_PRICE,
            min_gas_limit=Intent.DEFAULT_MIN_GAS_LIMIT,
            expiration=int(time()) + 365 * 86400
    ):
        self.to = contract_address
        self.value = value
        self.dependencies = dependencies
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.expiration = expiration

        if isinstance(data, bytes):
            self.data = data.decode()
        else:
            self.data = data

        assert(is_address(self.to))

class SignedIntent(object):
    def __init__(self, intent, wallet, signature):
        self.intent = intent
        self.wallet = wallet
        self.signature = signature
        self.id = intent.id(wallet)
    
    def to_json(self):
        return {
            "id": self.id,
            "dependencies": self.intent.dependencies,
            "wallet": self.wallet.address,
            "tx": {
                "to": self.intent.to,
                "value": self.intent.value,
                "data": self.intent.data,
                "maxGasPrice": self.intent.max_gas_price,
                "minGasLimit": self.intent.min_gas_limit,
            },
            "salt": self.intent.salt,
            "signer": self.wallet.signer,
            "expiration": self.intent.expiration,
            "signature": self.signature
        }

    def status(self, provider = None):
        if not provider:
            provider = global_provider()
            assert provider

        w3 = provider.web3
        contract = w3.eth.contract(abi = json.loads(wallet_abi), address = self.wallet.address)

        try:
            block = contract.call().relayedAt(Web3.toBytes(hexstr=self.id))
        except BadFunctionCallOutput:
            return StatusReceipt(Status.pending)

        if block != 0:
            relayer = contract.call().relayedBy(Web3.toBytes(hexstr=self.id))
            relay_event = w3.manager.request_blocking(
                "eth_getLogs",
                [{
                    'fromBlock': hex(block),
                    'toBlock': hex(block),
                    'address': self.wallet.address,
                    'topics': [None, self.id]
                }],
            )

            event_data = decode_receipt_event(relay_event[0]["data"])

            print(relay_event)

            return StatusReceipt(
                Status.completed,
                IntentReceipt(
                    relay_event[0]["tx_hash"],
                    relayer,
                    block,
                    event_data["success"]
                )
            )
        
        return StatusReceipt(Status.pending)

    def relay(self, provider = None):
        if not provider:
            provider = deglobal_provider()
            assert provider

        return requests.post(provider.relayer + "/relay", json=self.to_json())
