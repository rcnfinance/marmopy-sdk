
from marmopy import Action

ETH_NODE = "https://ropsten.node.rcn.loans:8545/"
RELAYER = "http://ec2-18-188-99-203.us-east-2.compute.amazonaws.com/"
TEST_ERC20 = "0x2f45b6fb2f28a73f110400386da31044b2e953d4"
TEST_CONTRACT = "0x1b1c4DC3102abEBE4c469ABA74cc94C381C62010"

class CallTestContract:
    def __init__(self, address):
        self.address = address
        
    @Action
    def fail1(self): return '' # TODO: fail1 should have no return

    @Action
    def call2(self): return 'string'

    @Action
    def call3(self): return 'address,uint256'
