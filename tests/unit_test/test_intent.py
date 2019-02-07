import unittest
from marmopy import ETH, ERC20, Intent, Wallet
from marmopy import Conf

class IntentTests(unittest.TestCase):
    def setUp(self):
        self.conf = Conf(
            "0xd586145101ec2c83174d91f2dd8df4b0cdb335f8f77935be590114916b535944",
            "0x68EA020095c1B3E58687cfA8eC2D631137Db28d7",
            "0x4E0B13eDeE810702884b72DBE018579Cb2e4C6fA",
            "0x6B0F919A5d450Fa5e6283Ff6178dC1FCd195FD2A",
            999
        )

        self.tokenContractAddress = "0x6Eb29e4Dffcbe467b755DCBa6fDdfA91F6f747e1"
        self.wallet = Wallet("0x5ef1dbf8ef171b33cd72a5d11b713442dcd2c70695753a0f6df9b38136e08d54", self.conf)

        self.erc20 = ERC20(self.tokenContractAddress)

    def test_transfer(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 4)

        intent = Intent(intent_action=intent_action, expiration=1549218987, max_gas_limit=0, max_gas_price=10 ** 32)

        self.assertEqual(intent.id(self.wallet), "0x4c8965758ff35849a98a26d322198d65467cbf1205311377ec8d3639217e654b")

    def test_transfer_named_parameters(self):
        intent_action = self.erc20.transfer({"to": "0x009ab4de1234c7066197d6ed75743add3576591f", "value": 4})

        intent = Intent(intent_action=intent_action, expiration=1549218987, max_gas_limit=0, max_gas_price=10 ** 32)
        self.assertEqual(intent.id(self.wallet), "0x4c8965758ff35849a98a26d322198d65467cbf1205311377ec8d3639217e654b")

    def test_transfer_eth(self):
        intent_action = ETH.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 1)

        intent = Intent(intent_action=intent_action, expiration=10 ** 24, max_gas_price=10 ** 32, max_gas_limit=0, salt="0x111151")

        self.assertEqual(intent.id(self.wallet), "0xe5e4e756b52ca2697f56a13bd4039d09885c56e051c54fbeff40076851d8ab76")

    def test_intent_with_dependency(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 100 * 10 ** 18)

        dependency_signed_intent = self.wallet.sign(Intent(
            intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 0),
            max_gas_limit=0, max_gas_price=9999999999, expiration = 10 ** 32
        ))

        intent = Intent(intent_action=intent_action, max_gas_limit=0, max_gas_price=9999999999, expiration=10 ** 36)
        intent.add_dependency(dependency_signed_intent)

        self.assertEqual(
            intent.id(self.wallet),
            "0x69f9e0539c6d1b349ce4c0c899d3a76f1118dc207e724d196bf9fb1c4fc957f3"
        )

    def test_intent_with_dependency_in_constructor(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 100 * 10 ** 18)

        dependency_signed_intent = self.wallet.sign(Intent(
            intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 0),
            max_gas_limit=0, max_gas_price=9999999999, expiration = 10 ** 32
        ))

        intent = Intent(intent_action=intent_action, expiration=10 ** 36, max_gas_limit=0, max_gas_price=9999999999, intent_dependencies=[dependency_signed_intent])

        self.assertEqual(
            intent.id(self.wallet),
            "0x69f9e0539c6d1b349ce4c0c899d3a76f1118dc207e724d196bf9fb1c4fc957f3"
        )

    def test_sign_intent(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 100 * 10 ** 18)

        intent = Intent(intent_action=intent_action, max_gas_limit=0, max_gas_price=9999999999, expiration=10 ** 36)

        signed_intent = self.wallet.sign(intent)
        self.assertEqual(signed_intent.signature, {
            'r': '0x57d3e232917a0e9be2670f57e5694ff445d1b91f9bdc17a85daab98d719b2b14',
            's': '0x2edd48c9f25ee8037bce2ffad51442b83451cbb57f12a7134268a0c1dcca0a40',
            'v': '0x1c'
        })

if __name__ == '__main__':
    unittest.main()
