from marmopy.utils import keccak256,toHexStringNoPrefixZeroPadded,remove_0x_prefix
from eth_utils import is_address

class Intent:
    MAX_GAS_PRICE = 9999999999
    MIN_GAS_PRICE = 0
    SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'
    
    def __init__(self,intentAction, signer, wallet,dependencies=list(), salt=SALT, maxGasPrice=MAX_GAS_PRICE, minGasLimit=MIN_GAS_PRICE):
        self.to = intentAction.contractAddress
        self.value = intentAction.value
        self.data = intentAction.encoded
        self.dependencies = dependencies
        self.signer = signer
        self.wallet = wallet
        self.salt = salt
        self.maxGasPrice = maxGasPrice
        self.minGasLimit = minGasLimit
        self.id = self._generateId()
        
        assert(is_address(self.signer))
        assert(is_address(self.wallet))
        assert(is_address(self.to))
        
    def __setattr__(self, name, value):
        if len(self.__dict__)<10:
            super().__setattr__(name, value)
        else:
            if name in self.__dict__.keys():
                super().__setattr__(name, value)
                super().__setattr__("id", self._generateId())
            else:
                raise Exception("Adding new variables not allowed.")
            

    def __repr__(self):
        return str(self.__dict__)
    
    
    def _generateId(self):
        encodedPackedBuilder = []
        
        encodedPackedBuilder.append(self.wallet)
        dependencies = "".join(map(remove_0x_prefix,self.dependencies))                      
        encodedPackedBuilder.append(keccak256("0x"+dependencies if dependencies!="" else dependencies))             
        encodedPackedBuilder.append(remove_0x_prefix(self.to))                 
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.value))              
        encodedPackedBuilder.append(keccak256(self.data))
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.minGasLimit))
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.maxGasPrice))
        encodedPackedBuilder.append(remove_0x_prefix(self.salt))      
        encodedPackedBuilder = "".join(encodedPackedBuilder)
        
        return "0x"+keccak256(encodedPackedBuilder)
    
    def sign(self,credentials):
        results = self.__dict__.copy()
        results["tx"] = {}
        for tx_key in ["to","value","data","minGasLimit","maxGasPrice"]:
            results["tx"][tx_key] = results.pop(tx_key)
            
        results["signature"] = credentials.signHash(self.id)
        
        return results
    
