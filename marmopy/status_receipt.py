from enum import Enum

StatusCode = Enum('pending', 'settling', 'completed')

class StatusReceipt(object):
    def __init__(self, code, receipt = None):
        self.code = code
        self.receipt = receipt

class IntentReceipt(object):
    def __init__(self, tx_hash, relayer, block_number, success):
        self.tx_hash = tx_hash
        self.relayer = relayer
        self.block_number = block_number
        self.success = success
