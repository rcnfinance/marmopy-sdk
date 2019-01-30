import unittest
from marmopy import IntentAction


class IntentTests(unittest.TestCase):

    def test_invalid_data_types(self):
        class ContractTest:
            @IntentAction
            def balanceOf(self, who='str'):
                return 'uint256'

        contract = ContractTest()
        address = "0x7F5EB5bB5cF88cfcEe9613368636f458800e62CB"

        with self.assertRaises(TypeError):
            contract.balanceOf(address)

    def test_invalid_arguments_types(self):
        class ContractTest:
            @IntentAction
            def balanceOf(self, who='address'):
                return 'uint256'

        contract = ContractTest()
        address = 123

        with self.assertRaises(TypeError):
            contract.balanceOf(address)

    def test_invalid_syntax(self):

        with self.assertRaises(TypeError):
            class ContractTest:
                @IntentAction
                def balanceOf(self, who):
                    pass


if __name__ == '__main__':
    unittest.main()
