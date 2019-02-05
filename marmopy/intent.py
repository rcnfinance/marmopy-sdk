import requests

from eth_utils import (
    remove_0x_prefix,
    function_abi_to_4byte_selector
)
from marmopy.utils import (
    keccak256,
    to_padded,
    to_bytes_32,
    to_hex_string_no_prefix_zero_padded
)
from eth_utils import is_address
from time import time
from .provider import global_provider
from .constants import wallet_abi
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from .utils import decode_receipt_event, from_bytes, to_bytes
from web3.contract import Contract as Web3Contract
import json

class Intent(object):
    DEFAULT_SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'
    DEFAULT_MIN_GAS_LIMIT = 0
    DEFAULT_MAX_GAS_PRICE = 9999999999

    def __init__(
        self,
        intent_action,
        intent_dependencies = None,
        salt = DEFAULT_SALT,
        max_gas_price = DEFAULT_MAX_GAS_PRICE,
        min_gas_limit = DEFAULT_MIN_GAS_LIMIT,
        expiration = int(time()) + 365 * 86400 # 1 year from now
    ):
        if not intent_dependencies:
            intent_dependencies = []

        self.to = intent_action["to"]
        self.value = intent_action["value"]
        self.data = intent_action["data"]
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.expiration = expiration
        self.intent_dependencies = []

        for intent in intent_dependencies:
            self.add_dependency(intent)

        assert(is_address(self.to))

    def id(self, wallet):
        encode_packed = [
            wallet.address,
            remove_0x_prefix(wallet.config.implementation),
            keccak256(self.prepare_implement_call(wallet.config))
        ]

        return "0x" + keccak256("".join(encode_packed))

    def prepare_implement_call(self, config):
        deps = self.prepare_dependency(config)

        deps_len = len(to_bytes(deps))
        deps_len_padded_dif = 32 - deps_len % 32
        deps_len_padded_dif = (deps_len_padded_dif, 0)[deps_len_padded_dif == 32]
        deps_len_padded = deps_len_padded_dif + deps_len

        data_len = len(to_bytes(self.data))
        data_len_padded_dif = 32 - data_len % 32
        data_len_padded_dif = (data_len_padded_dif, 0)[data_len_padded_dif == 32]

        implement_call = [
            "0x",
            to_hex_string_no_prefix_zero_padded(256),
            to_padded(self.to),
            to_hex_string_no_prefix_zero_padded(self.value),
            to_hex_string_no_prefix_zero_padded(256 + 32 + deps_len_padded),
            to_hex_string_no_prefix_zero_padded(self.min_gas_limit),
            to_hex_string_no_prefix_zero_padded(self.max_gas_price),
            to_hex_string_no_prefix_zero_padded(self.expiration),
            to_bytes_32(self.salt),
            to_hex_string_no_prefix_zero_padded(deps_len),
            remove_0x_prefix(deps),
            remove_0x_prefix(from_bytes(to_bytes("00") * deps_len_padded_dif)),
            to_hex_string_no_prefix_zero_padded(data_len),
            remove_0x_prefix(self.data),
            remove_0x_prefix(from_bytes(to_bytes("00") * data_len_padded_dif))
        ]
        
        return "".join(implement_call)

    def add_dependency(self, dependency):
        if isinstance(dependency, SignedIntent):
            dependency = {
                'address': dependency.wallet.address,
                'id': dependency.id
            }
        
        self.intent_dependencies.append(dependency)

    def prepare_dependency(self, config):
        deps_count = len(self.intent_dependencies)

        if deps_count == 0:
            # No intent_dependencies, no dependency
            return "0x"
        elif deps_count == 1:
            # Single dependency, call waller directly
            relayed_at_abi = {
                'name': 'relayedAt',
                'inputs': [
                    {
                        'type': 'bytes32',
                        'name': '_id'
                    }
                ]
            }

            to = to_bytes(self.intent_dependencies[0]['address'])
            data_signature = function_abi_to_4byte_selector(relayed_at_abi)
            data_params = to_bytes(Web3Contract._encode_abi(
                relayed_at_abi,
                [to_bytes(self.intent_dependencies[0]['id'])]
            ))

            return from_bytes(to + data_signature + data_params)
        else:
            # Multiple dependencies, using DepsUtils contract
            multiple_deps_abi = {
                'name': 'multipleDeps',
                'inputs': [
                    {
                        'type': 'address[]',
                        'name': '_wallets'
                    },
                    {
                        'type': 'bytes32[]',
                        'name': '_ids'
                    }
                ]
            }

            to = to_bytes(config.dependency_utils)
            data_signature = function_abi_to_4byte_selector(multiple_deps_abi)
            data_params = to_bytes(Web3Contract._encode_abi(multiple_deps_abi,
                [
                    list(map(lambda x: x["address"], self.intent_dependencies)),
                    list(map(lambda x: to_bytes(x["id"]), self.intent_dependencies))
                ]
            ))

            return from_bytes(to + data_signature + data_params)

class SignedIntent(object):
    def __init__(self, intent, wallet, signature):
        self.intent = intent
        self.wallet = wallet
        self.signature = signature
        self.id = intent.id(wallet)
    
    def to_json(self):
        return {
            "id": self.id,
            "wallet": self.wallet.address,
            "signer": self.wallet.signer,
            "signature": self.signature,
            "intent": {
                "implementation": self.wallet.config.implementation,
                "data": self.intent.prepare_implement_call(self.wallet.config),
                "detail": {
                    "dependency": self.intent.prepare_dependency(self.wallet.config),
                    "to": self.intent.to,
                    "value": self.intent.value,
                    "data": self.intent.data,
                    "maxGasPrice": self.intent.max_gas_price,
                    "minGasLimit": self.intent.min_gas_limit,
                    "salt": self.intent.salt,
                    "expiration": self.intent.expiration
                }
            }
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
            return { 'code': 'pending' }

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

            # TODO: Search by topic
            event_data = decode_receipt_event(relay_event[1]["data"])
            
            if 'tx_hash' in relay_event[1]:
                tx_hash = relay_event[1]["tx_hash"]
            else:
                tx_hash = relay_event[1]["transactionHash"]

            return {
                'code': 'completed',
                'receipt': {
                    'tx_hash': tx_hash,
                    'relayer': relayer,
                    'block_number': block,
                    'success': event_data["success"]
                }
            }
        else:
            return { 'code': 'pending' }

    def relay(self, provider = None):
        if not provider:
            provider = global_provider()
            assert provider

        return requests.post(provider.relayer + "v2/relay", json=self.to_json())
