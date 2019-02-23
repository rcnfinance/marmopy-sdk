import os

from marmopy import ERC20, Provider, DefaultConf, Wallet, Intent, from_bytes, Contract

from config import ETH_NODE, TEST_ERC20, RELAYER, CallTestContract, TEST_CONTRACT
from utils import wait_until

import time

DefaultConf.ROPSTEN.as_default()
Provider(ETH_NODE, RELAYER).as_default()

wallet = Wallet(from_bytes(os.urandom(32)))

success_intents = []

abi_test_contract = """
[{"constant":false,"inputs":[],"name":"call2","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"fail2","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"fail1","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"fail3","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"call3","outputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"call1","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
"""

def test_relay_and_read_status_success():
    wallet_receiver = Wallet(from_bytes(os.urandom(32)))

    intent_action = ERC20(TEST_ERC20).transfer(wallet_receiver.address, 0)
    intent = Intent(intent_action = intent_action)

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0]

def test_relay_and_read_status_error():
    intent_action = CallTestContract(TEST_CONTRACT).fail1()
    intent = Intent(intent_action = intent_action)

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert not signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["error"] == "This is the error 1"

def test_relay_with_dependency_and_read_status_success():
    wallet_receiver = Wallet(from_bytes(os.urandom(32)))

    intent_action = ERC20(TEST_ERC20).transfer(wallet_receiver.address, 0)
    intent = Intent(intent_action = intent_action)
    intent.add_dependency(success_intents[0])

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0]

def test_relay_with_multiple_dependency_and_read_status_success():
    wallet_receiver = Wallet(from_bytes(os.urandom(32)))

    intent_action = ERC20(TEST_ERC20).transfer(wallet_receiver.address, 0)
    intent = Intent(intent_action = intent_action)
    intent.add_dependency(success_intents[0])
    intent.add_dependency(success_intents[1])
    intent.add_dependency(success_intents[2])

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0]

def test_read_receipt():
    intent_action = CallTestContract(TEST_CONTRACT).call2()
    intent = Intent(intent_action = intent_action, salt=from_bytes(os.urandom(32)))

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0] == "This is the return of the call2"

def test_read_receipt_abi():
    intent_action = Contract(abi_test_contract)(TEST_CONTRACT).call2()
    intent = Intent(intent_action = intent_action, salt=from_bytes(os.urandom(32)))

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0] == "This is the return of the call2"

def test_read_receipt_multiple():
    intent_action = CallTestContract(TEST_CONTRACT).call3()
    intent = Intent(intent_action = intent_action, salt=from_bytes(os.urandom(32)))

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0] == wallet.address
    assert signed_intent.status()["receipt"]["result"]["output"][1] == int(wallet.address, 16) * 9

def test_read_receipt_multiple_abi():
    intent_action = Contract(abi_test_contract)(TEST_CONTRACT).call3()
    intent = Intent(intent_action = intent_action, salt=from_bytes(os.urandom(32)))

    signed_intent = wallet.sign(intent)

    response = signed_intent.relay()

    assert response.status_code == 201
    assert wait_until(lambda: signed_intent.status()["code"] == "completed", 640)
    time.sleep(5)

    assert signed_intent.status()["receipt"]["success"]
    success_intents.append(signed_intent)
    assert signed_intent.status()["receipt"]["result"]["output"][0] == wallet.address
    assert signed_intent.status()["receipt"]["result"]["output"][1] == int(wallet.address, 16) * 9
