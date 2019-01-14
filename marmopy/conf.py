
def global_conf():
    global glob_conf
    return glob_conf 

class Conf:
    def __init__(self, init_code, factory, network):
        self.init_code = init_code
        self.factory = factory
        self.network = network

    def as_default(self):
        global glob_conf
        glob_conf = self

class DefaultConf:
    ROPSTEN = Conf("0x5cde6918eab87f0d3828841c5e63362b583d34513a2a64dd32c5d033d252937b", "0x1053deb5e0f1697289b8a1b11aa870f07a7fb221", 3)
