from marmopy import Action
from .ERC20 import ERC20

class WETH(ERC20):
    @Action
    def deposit(self, value="payable"): pass

    @Action
    def withdraw(self, value="uint256"): pass
