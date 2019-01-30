import os

from examples import ERC20
from marmopy import Provider, DefaultConf, Wallet, Intent, from_bytes

from config import ETH_NODE, TEST_ERC20, RELAYER, CallTestContract, TEST_CONTRACT
from utils import wait_until

import time

DefaultConf.ROPSTEN.as_default()
Provider(ETH_NODE, RELAYER).as_default()

wallet = Wallet(from_bytes(os.urandom(32)))

success_intents = []

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
