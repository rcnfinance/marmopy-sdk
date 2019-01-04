from marmopy.utils import keccak256,toHexStringNoPrefixZeroPadded,remove_0x_prefix
from eth_utils import is_address


class Intent(object):
    
    MAX_GAS_PRICE = 9999999999

    MIN_GAS_PRICE = 0

    SALT = '0x0000000000000000000000000000000000000000000000000000000000000000'

    BYTECODE_1 = "6080604052348015600f57600080fd5b50606780601d6000396000f3fe6080604052366000803760008036600073"

    BYTECODE_2 = "5af43d6000803e8015156036573d6000fd5b3d6000f3fea165627a7a7230582033b260661546dd9894b994173484da72335f9efc37248d27e6da483f15afc1350029"

    MARMO_FACTORY_ADDRESS = "1053deb5e0f1697289b8a1b11aa870f07a7fb221"

    MARMO_ADDRESS = "3618a379f2624f42c0a8c79aad8db9d24d6e0312"
    
    EXPIRATION = 15

    def __init__(self,intentAction, signer, wallet=None,dependencies=list(), salt=SALT, maxGasPrice=MAX_GAS_PRICE, minGasLimit=MIN_GAS_PRICE, expiration=EXPIRATION):
        self.to = intentAction.contractAddress
        self.value = intentAction.value
        self.data = intentAction.encoded
        self.dependencies = dependencies
        self.signer = signer
        self.wallet = wallet if wallet else self._generateWalletAddress(self.signer)
        self.salt = salt
        self.maxGasPrice = maxGasPrice
        self.minGasLimit = minGasLimit
        self.expiration = expiration
        self.id = self._generateId()
        
        assert(is_address(self.signer))
        assert(is_address(self.wallet))
        assert(is_address(self.to))
        
    def __setattr__(self, name, value):
        if len(self.__dict__)<11:
            super(Intent,self).__setattr__(name, value)
        else:
            if name in self.__dict__.keys():
                super(Intent,self).__setattr__(name, value)
                super(Intent,self).__setattr__("id", self._generateId())
            else:
                raise Exception("Adding new variables not allowed.")
            

    def __repr__(self):
        return str(self.__dict__)
    
    
    def _generateId(self):
        encodedPackedBuilder = []
        
        encodedPackedBuilder.append(self.wallet)
        dependencies = "".join(map(remove_0x_prefix,self.dependencies))                      
        encodedPackedBuilder.append(keccak256(dependencies))             
        encodedPackedBuilder.append(remove_0x_prefix(self.to))                 
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.value))              
        encodedPackedBuilder.append(keccak256(self.data))
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.minGasLimit))
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.maxGasPrice))
        encodedPackedBuilder.append(remove_0x_prefix(self.salt)) 
        encodedPackedBuilder.append(toHexStringNoPrefixZeroPadded(self.expiration))
        encodedPackedBuilder = "".join(encodedPackedBuilder)
        
        return "0x"+keccak256(encodedPackedBuilder)
    
    def _generateWalletAddress(self,signer):
    
        signer = signer.replace("0x","")

        initCode  = keccak256(Intent.BYTECODE_1 + Intent.MARMO_ADDRESS + Intent.BYTECODE_2)

        byte = "ff"

        concat = byte + Intent.MARMO_FACTORY_ADDRESS + signer + initCode

        address = bytearray.fromhex(keccak256(concat))

        return "0x"+address[-20:].hex()
    
    
    def sign(self,credentials):
        results = self.__dict__.copy()
        results["tx"] = {}
        for tx_key in ["to","value","data","minGasLimit","maxGasPrice"]:
            results["tx"][tx_key] = results.pop(tx_key)
            
        results["signature"] = credentials.signHash(self.id)
        
        return results
    
