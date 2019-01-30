from marmopy import Wallet
from marmopy import Intent, IntentAction, DefaultConf
from time import time, sleep
from marmopy import Intent, IntentGeneric	
from examples.generic_contract import Contract	
from marmopy import Provider

DefaultConf.ROPSTEN.as_default()

utime = str(time()).replace(".", "")
wallet = Wallet("0x" + ("0" * (64 - len(utime))) + utime)

abi = """	
[	
{	
"constant":false,	
"inputs":[	
	{	
		"name":"_to",	
		"type":"address"	
	},	
	{	
		"name":"_value",	
		"type":"uint256"	
	}	
],	
"name":"transfer",	
"outputs":[	
	{	
		"name":"success",	
		"type":"bool"	
	}	
],	
"payable":false,	
"type":"function"	
}	
]	
"""	

token_contract_address = "0x2f45b6fb2f28a73f110400386da31044b2e953d4" #RCN TOKEN	
to = "0xA6693e041aAfE9b9D722338Ca9f8A6e7746d7148"	
data = Contract(abi).transfer({"_to":to, "_value":0})	

intent = IntentGeneric(data, token_contract_address, 0)
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})

intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})
intent.add_dependency({'address':'0x3842d899c6ebccec96cf6725f050349c7d5c2520', 'id': '0x22db790771a4d0c8c58553ed08e77b06c4ca11a8620e2d04e40f161c63fbd8ed'})

signedIntent = wallet.sign(intent)

intent2 = IntentGeneric(data, token_contract_address, 0)
intent2.add_dependency(signedIntent)

# signedIntent.relay("http://localhost:8081/relay")

provider = Provider("https://ropsten.node.rcn.loans:8545/", "http://ec2-18-188-99-203.us-east-2.compute.amazonaws.com/")
# provider = Provider("https://ropsten.node.rcn.loans:8545/", "http://localhost:8081/")

signedIntent.relay(provider)
# wallet.sign(intent2).relay(provider)

intent3 = IntentGeneric(data, token_contract_address, 1)
# wallet.sign(intent3).relay(provider)

print(signedIntent.id)

signedIntent.status(provider)