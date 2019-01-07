from marmopy import IntentAction

class ERC20:
    def __init__(self,contractAddress):
        self.contractAddress = contractAddress
        
    @IntentAction
    def totalSupply(self): return 'uint256'
    
    @IntentAction
    def balanceOf(self, who='address'): return 'uint256'
    
    @IntentAction
    def allowance(self, owner='address', spender='address'): return 'uint256'
    
    @IntentAction
    def transfer(self, to='address', value='uint256'): return 'bool'
    
    @IntentAction
    def approve(self, spender='address', value='uint256') : return 'bool'
    
    @IntentAction
    def transferFrom(self, _from='address', to='address', value='uint256'): return 'bool'