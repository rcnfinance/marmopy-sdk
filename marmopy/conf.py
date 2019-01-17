
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
    ROPSTEN = Conf("0x98ef25e9f596000233ed019f909cc8a5f35984f1cc0b0b9e05407ce7a6820bc1", "0x6306b6a26c70c03279c037f630be03046104cb37", 3)