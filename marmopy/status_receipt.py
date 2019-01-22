from enum import Enum

Status = Enum('pending', 'settling', 'completed')

class StatusReceipt(object):
    def __init__(self, status, receipt = None):
        self.status = status
        self.receipt = receipt

class IntentReceipt(object):
    def __init__(self, tx_hash, relayer, block_number, success):
        self.tx_hash = tx_hash
        self.relayer = relayer
        self.block_number = block_number
        self.success = success
