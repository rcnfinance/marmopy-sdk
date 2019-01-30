
class ETH:
    @staticmethod
    def transfer(to, value):
        return {
            "to": to,
            "value": value,
            "data": "0x"
        }
