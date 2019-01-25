
def global_conf():
    global glob_conf
    return glob_conf 

class Conf:
    def __init__(self, init_code, factory, dependency_utils, network):
        self.init_code = init_code
        self.factory = factory
        self.dependency_utils = dependency_utils
        self.network = network

    def as_default(self):
        global glob_conf
        glob_conf = self

class DefaultConf:
    ROPSTEN = Conf(
        "0x230df5d90f2bed3911a7e00dc17f6497be9b79785d80d99dd2bb639b9f43a7d4",
        "0xFCdDEFed943B395d99c71fE6E64a8027761e1bDF",
        "0x874ad09c8ab7da34bf75550409e9446b47558364",
        3
    )
