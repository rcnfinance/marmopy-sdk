
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
        "0x674bd4d0754e3809fb963174498670c4df41f20f7f1b1470897f5239fa7d2518",
        "0xceb46ecca6aac8e5dbc7f2e340c77eb86351a2e0",
        "0x035dfc65c9995e81db28c9ed81326595719a5bfd",
        "0x874ad09c8ab7da34bf75550409e9446b47558364",
        3
    )
