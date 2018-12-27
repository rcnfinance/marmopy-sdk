import unittest
from marmopy import Intent,Credentials
from examples import ERC20


class IntentTests(unittest.TestCase):
    def setUp(self):
        self.tokenContractAddress = "0x2f45b6fb2f28a73f110400386da31044b2e953d4"
        
        self.to = "0x7F5EB5bB5cF88cfcEe9613368636f458800e62CB"
        
        self.credentials = Credentials("512850c7ebe3e1ade1d0f28ef6eebdd3ba4e78748e0682f8fda6fc2c2c5b334a")
        
        self.erc20 = ERC20(self.tokenContractAddress)
        
    def testTransfer(self):
        value = 1

        intentAction = self.erc20.transfer(self.to,value)

        contractAddress = "0xDc3914BEd4Fc2E387d0388B2E3868e671c143944"

        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress)

        self.assertEqual(intent.id, "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928")
        
    def testBalanceOf(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress)
        
        self.assertEqual(intent.id, "0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e")
        
        
    def testBalanceOfWithDependencies(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e"]
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, dependencies=dependencies)
        
        self.assertEqual(intent.id, "0x19ca8e36872eaf21cd75c9319cfd08769b61fcb7c8ab119d71960c27585595af")
        
        new_dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                            "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        intent.dependencies = new_dependencies
        
        self.assertEqual(intent.id, "0xab4b18a2b163ac552a6d2eac23529e4d5e25ff54c41831b75e8c169a03f39a20")
        
        
    def testBalanceOfWithCustomGasPrices(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
       
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies, maxGasPrice=999999, minGasLimit=300000)
        
        self.assertEqual(intent.id, "0x9ef832fe6023c21990339fe87724fe5a19fdb4697ce32769c238eb6ab9b92b2c")
        
        
    def testBalanceOfWithCustomSalt(self):
        
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000)
        
        self.assertEqual(intent.id, "0xfc1e9fd25abd26a1be78817f0675a5051285af23957ca0322f2925d93f291ec5")
        
        intent.salt = "0x0000000000000000000000000000000000000000000000000000000000000002"
        
        self.assertEqual(intent.id, "0xacd5d801cecc1790b95c5395e4f48a40d964ae0c6b70051b3c907060e67da079")
        
    # Output should be same as marmoj IntentRequestTransformer output.
    # Can be used like this: requests.post("http://ec2-3-16-37-20.us-east-2.compute.amazonaws.com/relay",json=intent.sign(credentials))
    def testSignIntent(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000)
        
        signedIntent = intent.sign(self.credentials)
        
        expected = {'id': '0xfc1e9fd25abd26a1be78817f0675a5051285af23957ca0322f2925d93f291ec5',
                    'dependencies': ['0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e',
                                     '0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928'],
                    'wallet': '0xbbf289d846208c16edc8474705c748aff07732db',
                    "tx":{
                        'to': '0x2f45b6fb2f28a73f110400386da31044b2e953d4',
                        'value': 0,
                        'data': '0x70a082310000000000000000000000007f5eb5bb5cf88cfcee9613368636f458800e62cb',
                        'minGasLimit': 300000,
                        'maxGasPrice': 999999,
                    },
                    'salt': '0x0000000000000000000000000000000000000000000000000000000000000001',
                    'signer': '0x9d7713f5048c270d7c1dBe65F44644F4eA47f774',
                    'signature': {'r': '0xb0f341f6afae65a4ce091584d5b3d6548b9c0727346355a6c23bb5e9ef7a8787',
                                  's': '0x78b9e0bf96b838140201e574e550a66ce3fd8ea55270f9f1fb041ecbe78524b1',
                                  'v': '0x1c'}}
        
        self.assertEqual(signedIntent,expected)
        
        
if __name__ == '__main__':    
    unittest.main()
