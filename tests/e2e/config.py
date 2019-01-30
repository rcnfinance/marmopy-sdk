
from marmopy import IntentAction

ETH_NODE = "https://ropsten.node.rcn.loans:8545/"
RELAYER = "http://ec2-18-188-99-203.us-east-2.compute.amazonaws.com/"
TEST_ERC20 = "0x2f45b6fb2f28a73f110400386da31044b2e953d4"
TEST_CONTRACT = "0x1b1c4DC3102abEBE4c469ABA74cc94C381C62010"

class CallTestContract:
    def __init__(self, contractAddress):
        self.contractAddress = contractAddress
        
    @IntentAction
    def fail1(self): return 'bool' # TODO: fail1 should have no return
