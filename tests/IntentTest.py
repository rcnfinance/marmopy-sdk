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

        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, expiration=15)

        self.assertEqual(intent.id, "0x7935c8f49cb284e1c5c8dd95b3fc6c9cad6519a17555a5f2e43f9aaa31d25a37")
        
    def testBalanceOf(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, expiration=15)
        
        self.assertEqual(intent.id, "0x0dd96a883c69dca2fef7de903ed543b2751919592a799902aa84ce7ed6a23479")
        
    def testBalanceoffWithWalletGeneration(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), expiration=15)
        self.assertEqual(intent.wallet,'0x8bdd988a19f5c9fb82bd98797ac78c1f48bd5af8')
        
        self.assertEqual(intent.id, '0xf914432e0e9739b4ee726c1e52579f6d2e96cacac8bc391d3ffeae579372ade3')
        
    def testBalanceOfWithDependencies(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e"]
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, dependencies=dependencies, expiration=15)
        
        self.assertEqual(intent.id, "0x5de183da65683636ad564c80559c6cf68d5c738239f15da75e5a020d039cf7fb")
        
        new_dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                            "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        intent.dependencies = new_dependencies
        
        self.assertEqual(intent.id, "0x0d42d9890e1c0cca4d56ec5b532e6f7f1597f5cda57a0c1726f0eb25d2bc4a26")
        
        
    def testBalanceOfWithCustomGasPrices(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
       
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies, maxGasPrice=999999, minGasLimit=300000, expiration=15)
        
        self.assertEqual(intent.id,"0x40b7b0871f7b3e25020766c21545be0ef33349a949b6f4b9548387d4d539a110")
        
        
    def testBalanceOfWithCustomSalt(self):
        
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000, expiration=15)
        
        self.assertEqual(intent.id, "0x63bfa4961085e360ff2507256aae202ef05fe1883475eb21456796b81f5a0e58")
        
        intent.salt = "0x0000000000000000000000000000000000000000000000000000000000000002"
        
        self.assertEqual(intent.id, "0x6e78ee9f136303375275ad50c6f0823f5863a148d351552409685a8b491d3a98")
        
    def testBalanceOfWithCustomExpiration(self):
        
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000,expiration=30)
        
        self.assertEqual(intent.id, '0xb525cc7118165ae85c0761ce315a3ad4ab5899793f3c9c1f7804e6aa9fcd8534')
        
        
    # Output should be same as marmoj IntentRequestTransformer output.
    # Can be used like this: requests.post("http://ec2-3-16-37-20.us-east-2.compute.amazonaws.com/relay",json=intent.sign(credentials))
    def testSignIntent(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000, expiration=15)
        
        signedIntent = intent.sign(self.credentials)
        
        expected = {'id': "0x63bfa4961085e360ff2507256aae202ef05fe1883475eb21456796b81f5a0e58",
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
                    "expiration": 15,
                    'signature': {'r': '0x6381ad3f9c7a15b4a6bec0d21edef69b571de3a7cd5a03befb11468f2c7e19f4',
                                  's': '0x7c9e94006394b16150150d590a5c3beb06e46978e9b2a7c813199570ad6288bc',
                                  'v': '0x1b'}}
        
        self.maxDiff = None
        
        self.assertEqual(signedIntent,expected)
        
        
if __name__ == '__main__':    
    unittest.main()
