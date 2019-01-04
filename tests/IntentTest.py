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

        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, expiration=900000000)

        self.assertEqual(intent.id, "0x9e27e891d2949f942edc9416531a20ff6fef2a972ddc767f614842ec967664af")
        
    def testBalanceOf(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, expiration=900000000)
        self.assertEqual(intent.id, "0xd293e6875488c4ff30468ac42dd77f749dda9b795ef45ddaebb1b504280767e2")
        
        
    def testBalanceOfWithDependencies(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e"]
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress, dependencies=dependencies, expiration=900000000)
        
        self.assertEqual(intent.id, "0xcf98a4bb0686d7a29cade0f7305f2aa6b3b51c6ece02d2665b117e048373006d")
        
        new_dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                            "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        intent.dependencies = new_dependencies
        
        self.assertEqual(intent.id, "0xa13667b409ce93128bd2fe7b59772a965820dc0040563b9384425949785119d3")
        
        
    def testBalanceOfWithCustomGasPrices(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
       
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies, maxGasPrice=999999, minGasLimit=300000, expiration=900000000)
        
        self.assertEqual(intent.id, "0xefe84c88c6b513fbabe882ba45e9d921923972c0c7530153a31be54a0d135725")
        
        
    def testBalanceOfWithCustomSalt(self):
        
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000, expiration=900000000)
        
        self.assertEqual(intent.id, "0x2f4b78f9226c0c30962ed108407d0586b17ebc62c27a3c2658d60143eb0d9773")
        
        intent.salt = "0x0000000000000000000000000000000000000000000000000000000000000002"
        
        self.assertEqual(intent.id, "0xfc545c299d0c273f600a5914b2a1d3e9ea6740d293f5d4c519a6fad6d1936bec")
        
    # Output should be same as marmoj IntentRequestTransformer output.
    # Can be used like this: requests.post("http://ec2-3-16-37-20.us-east-2.compute.amazonaws.com/relay",json=intent.sign(credentials))
    def testSignIntent(self):
        intentAction = self.erc20.balanceOf(self.to)
        
        contractAddress = "0xbbf289d846208c16edc8474705c748aff07732db"
        
        dependencies = ["0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e",
                        "0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928"]
        
        salt = "0x0000000000000000000000000000000000000000000000000000000000000001"
        
        intent = Intent(intentAction=intentAction, signer=self.credentials.getAddress(), wallet=contractAddress,
                        dependencies=dependencies,salt=salt, maxGasPrice=999999, minGasLimit=300000, expiration=900000000)
        
        signedIntent = intent.sign(self.credentials)
        expected = {'id': '0x2f4b78f9226c0c30962ed108407d0586b17ebc62c27a3c2658d60143eb0d9773',
                    'dependencies': ['0xee2e1b62b008e27a5a3d66352f87e760ed85e723b6834e622f38b626090f536e',
                                     '0x6b67aac6eda8798297b1591da36a215bfbe1fed666c4676faf5a214d54e9e928'],
                    'wallet': '0xbbf289d846208c16edc8474705c748aff07732db',
                    "tx":{
                        'to': '0x2f45b6fb2f28a73f110400386da31044b2e953d4',
                        'value': 0,
                        'data': '0x70a082310000000000000000000000007f5eb5bb5cf88cfcee9613368636f458800e62cb',
                        'minGasLimit': 300000,
                        'maxGasPrice': 999999
                    },
                    'expiration': 900000000,
                    'salt': '0x0000000000000000000000000000000000000000000000000000000000000001',
                    'signer': '0x9d7713f5048c270d7c1dBe65F44644F4eA47f774',
                    'signature': {'r': '0xa0f036a79880eef92de985dacbf3999997dba735de3e611ffe06d0846ba08c10',
                                  's': '0x67d2b91afda986ec42e5e6cf33e4db8d2c53586c443a61c5ca2774dc6a83fa11',
                                  'v': '0x1b'}}
        
        self.assertEqual(signedIntent,expected)
        
        
if __name__ == '__main__':    
    unittest.main()
