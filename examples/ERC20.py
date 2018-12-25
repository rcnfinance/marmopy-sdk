from marmopy import IntentAction

class ERC20:
    def __init__(self,contractAddress):
        self.contractAddress = contractAddress
        
    @IntentAction
    def totalSupply(self) -> 'uint256': pass
    
    @IntentAction
    def balanceOf(self, who:'address') -> 'uint256': pass
    
    @IntentAction
    def allowance(self, owner:'address', spender:'address') ->'uint256': pass
    
    @IntentAction
    def transfer(self, to:'address', value:'uint256') -> 'bool': pass
    
    @IntentAction
    def approve(self, spender:'address', value:'uint256') -> 'bool': pass
    
    @IntentAction
    def transferFrom(self, _from:'address', to:'address', value:'uint256') -> 'bool': pass