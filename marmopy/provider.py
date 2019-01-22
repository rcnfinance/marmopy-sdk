from web3 import Web3, HTTPProvider
import warnings

def global_provider():
    global global_provider
    return global_provider 

class Provider:
    def __init__(self, web3, relayer):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        if isinstance(web3, Web3):
            self.web3 = web3
        else:
            self.web3 = Web3(HTTPProvider(web3))

        self.relayer = relayer

    def as_default(self):
        global global_provider
        global_provider = self
