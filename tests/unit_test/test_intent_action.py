import unittest
from marmopy import Action


class IntentTests(unittest.TestCase):

    def test_invalid_data_types(self):
        class ContractTest:
            def __init__(self, address):
                self.address = address

            @Action
            def balanceOf(self, who='str'):
                return 'uint256'

        contract = ContractTest("0x7F5EB5bB5cF88cfcEe9613368636f458800e62CB")
        address = "0x7F5EB5bB5cF88cfcEe9613368636f458800e62CB"

        with self.assertRaises(TypeError):
            contract.balanceOf(address)

    def test_invalid_arguments_types(self):
        class ContractTest:
            def __init__(self, address):
                self.address = address

            @Action
            def balanceOf(self, who='address'):
                return 'uint256'

        contract = ContractTest("0x7F5EB5bB5cF88cfcEe9613368636f458800e62CB")
        address = 123

        with self.assertRaises(TypeError):
            contract.balanceOf(address)

    def test_invalid_syntax(self):
        with self.assertRaises(TypeError):
            class ContractTest:
                @Action
                def balanceOf(self, who):
                    pass


if __name__ == '__main__':
    unittest.main()
