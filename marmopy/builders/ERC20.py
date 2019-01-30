from marmopy import Action

class ERC20:
    def __init__(self, address):
        self.address = address
        
    @Action
    def totalSupply(self): return 'uint256'
    
    @Action
    def balanceOf(self, who='address'): return 'uint256'
    
    @Action
    def allowance(self, owner='address', spender='address'): return 'uint256'
    
    @Action
    def transfer(self, to='address', value='uint256'): return 'bool'
    
    @Action
    def approve(self, spender='address', value='uint256') : return 'bool'
    
    @Action
    def transferFrom(self, _from='address', to='address', value='uint256'): return 'bool'
