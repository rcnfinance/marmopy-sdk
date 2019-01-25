import requests

from eth_utils import (
    remove_0x_prefix,
    function_abi_to_4byte_selector
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
from utils import decode_receipt_event
from web3.contract import Contract as Web3Contract
import json

class Intent(object):
    DEFAULT_SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'
    DEFAULT_MIN_GAS_LIMIT = 0
    DEFAULT_MAX_GAS_PRICE = 9999999999

    def __init__(
        self,
        intent_action,
        intent_dependencies = [],
        salt = DEFAULT_SALT,
        max_gas_price = DEFAULT_MAX_GAS_PRICE,
        min_gas_limit = DEFAULT_MIN_GAS_LIMIT,
        expiration = int(time()) + 365 * 86400 # 1 year from now
    ):
        self.to = intent_action.contractAddress
        self.value = intent_action.value
        self.data = intent_action.encoded
        self.intent_dependencies = intent_dependencies
        self.salt = salt
        self.max_gas_price = max_gas_price
        self.min_gas_limit = min_gas_limit
        self.expiration = expiration

        assert(is_address(self.to))

    def id(self, wallet):
        encoded_packed_builder = []
        encoded_packed_builder.append(wallet.address)
        encoded_packed_builder.append(keccak256(self.prepare_dependency(wallet.config)))
        encoded_packed_builder.append(remove_0x_prefix(self.to))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.value))
        encoded_packed_builder.append(keccak256(self.data))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.min_gas_limit))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.max_gas_price))
        encoded_packed_builder.append(remove_0x_prefix(self.salt))
        encoded_packed_builder.append(to_hex_string_no_prefix_zero_padded(self.expiration))
        encoded_packed_builder = "".join(encoded_packed_builder)
        return "0x" + keccak256(encoded_packed_builder)

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

            to = self.intent_dependencies[0]['address'].replace('0x', '').decode('hex')
            data_signature = function_abi_to_4byte_selector(relayed_at_abi)
            data_params = Web3Contract._encode_abi(
                relayed_at_abi,
                [self.intent_dependencies[0]['id'].replace('0x', '').decode('hex')]
            ).replace('0x', '').decode('hex')

            return '0x' + (to + data_signature + data_params).encode('hex')
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

            to = config.dependency_utils.replace('0x', '').decode('hex')
            data_signature = function_abi_to_4byte_selector(multiple_deps_abi)
            data_params = Web3Contract._encode_abi(multiple_deps_abi,
                [
                    map(lambda x: x["address"].replace('0x', '').decode('hex'), self.intent_dependencies),
                    map(lambda x: x["id"].replace('0x', '').decode('hex'), self.intent_dependencies)
                ]
            ).replace('0x', '').decode('hex')

            return '0x' + (to + data_signature + data_params).encode('hex')


class IntentGeneric(Intent):
    def __init__(
            self,
            data,
            contract_address,
            value,
            intent_dependencies=[],
            salt=Intent.DEFAULT_SALT,
            max_gas_price=Intent.DEFAULT_MAX_GAS_PRICE,
            min_gas_limit=Intent.DEFAULT_MIN_GAS_LIMIT,
            expiration=int(time()) + 365 * 86400
    ):
        self.to = contract_address
        self.value = value
        self.intent_dependencies = intent_dependencies
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
            "dependency": self.intent.prepare_dependency(self.wallet.config),
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

            event_data = decode_receipt_event(relay_event[0]["data"])

            return {
                'code': 'completed',
                'receipt': {
                    'tx_hash': relay_event[0]["tx_hash"],
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

        return requests.post(provider.relayer + "/relay", json=self.to_json())
