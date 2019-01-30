import unittest
from marmopy import Intent, Wallet
from examples import ERC20
from marmopy import Conf

class IntentTests(unittest.TestCase):
    def setUp(self):
        self.conf = Conf(
            "0xe814f48c2eaf753ae51c7c807e2b1736700126c58af556d78c7c6158d201a125",
            "0x4E0B13eDeE810702884b72DBE018579Cb2e4C6fA",
            "",
            999
        )

        self.tokenContractAddress = "0x6B0F919A5d450Fa5e6283Ff6178dC1FCd195FD2A"
        self.wallet = Wallet("0x5ef1dbf8ef171b33cd72a5d11b713442dcd2c70695753a0f6df9b38136e08d54", self.conf)

        self.erc20 = ERC20(self.tokenContractAddress)

    def test_transfer(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 4)

        intent = Intent(intent_action=intent_action, expiration=1548030494, max_gas_price=10 ** 32)
        self.assertEqual(intent.id(self.wallet), "0xe34f44ab2514803ba5f1a4766f5fe1d6d012a9599c8e13843962366f04427198")

    def test_intent_with_dependency(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 100 * 10 ** 18)

        dependency_signed_intent = self.wallet.sign(Intent(
            intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 0),
            expiration = 10 ** 32
        ))

        intent = Intent(intent_action=intent_action, expiration=10 ** 36)
        intent.add_dependency(dependency_signed_intent)

        self.assertEqual(
            intent.id(self.wallet),
            "0x0f1a91058c267c034e020aa4651b59e4d459ec7314225de3865217bec8bfefdc"
        )

    def test_sign_intent(self):
        intent_action = self.erc20.transfer("0x009ab4de1234c7066197d6ed75743add3576591f", 100 * 10 ** 18)

        intent = Intent(intent_action=intent_action, expiration=10 ** 36)

        signed_intent = self.wallet.sign(intent)
        self.assertEqual(signed_intent.signature, {
            'r': '0x99262472e0631b15dbc42b56765f40d42a205b10a3520e05d2c539d644572405',
            's': '0x482c78384f02c7cc6e3dad7a0dfad9f5b77a0da78148aa031fb482a06a3e28c',
            'v': '0x1c'
        })

if __name__ == '__main__':
    unittest.main()
