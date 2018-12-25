from functools import partial
from eth_utils import function_abi_to_4byte_selector,encode_hex
import web3
from web3.contract import encode_abi

class IntentAction:
    def __init__(self,function):
        self.abi = {}
        
        annotations = function.__annotations__.copy()
        
        self.abi['name'] = function.__name__
        
        if "return" not in annotations: raise TypeError("Invalid Syntax, no return datatype specified")
        
        self.abi['outputs'] = [{'name':'','type':annotations.pop("return")}]
        
        self.abi['inputs'] = [{"name":param.replace("_",""),"type":datatype} for param,datatype in annotations.items()]
        
        self.abi['type'] = "function"
        
    def __call__(self,*args):
        
        instance, arguments = args[0], args[1:]
        
        for attr,value in instance.__dict__.items(): setattr(self,attr,value)
    
        data = encode_hex(function_abi_to_4byte_selector(self.abi))
        
        self.encoded = encode_abi(web3,self.abi,arguments,data)
        
        self.arguments = dict(zip([arg['name'] for arg in self.abi['inputs']],arguments))
        
        return self
    
    def __get__(self,instance,_):           
        return partial(self.__call__, instance)
    
    def __repr__(self):
        return str(self.abi)
