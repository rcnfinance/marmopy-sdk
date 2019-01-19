
class Config:
    
    configured = False
    
    @classmethod
    def Create(cls, init_code, factory, network):
        cls.init_code = init_code
        cls.factory = factory
        cls.network = network
        cls.configured = True
    
    @classmethod
    def as_default(cls):
        cls.Create("0x98ef25e9f596000233ed019f909cc8a5f35984f1cc0b0b9e05407ce7a6820bc1", "0x6306b6a26c70c03279c037f630be03046104cb37", 3)
