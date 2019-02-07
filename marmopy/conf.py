
def global_conf():
    global glob_conf
    return glob_conf 

class Conf:
    def __init__(self, init_code, factory, implementation, dependency_utils, network):
        self.init_code = init_code
        self.factory = factory
        self.implementation = implementation
        self.dependency_utils = dependency_utils
        self.network = network

    def as_default(self):
        global glob_conf
        glob_conf = self

class DefaultConf:
    ROPSTEN = Conf(
        "0x14e25af98043632f65f78deb5c4b4cf0c299e2b2e34f034abfde94d138de6a7e",
        "0x534cbda9c0a9c5c29d0dced0d1d24127e3078519",
        "0x2101d39973a6a49061934e40f21db638874b39da",
        "0x874ad09c8ab7da34bf75550409e9446b47558364",
        3
    )
