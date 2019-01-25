wallet_abi = """	
[	
	{	
		"constant":true,	
		"inputs":[	
			{	
				"name":"_id",	
				"type":"bytes32"	
			}
		],	
		"name":"relayedAt",	
		"outputs":[	
			{	
				"name":"_block",	
				"type":"uint256"	
			}	
		],	
		"payable":false,	
		"type":"function"	
	},
    {	
		"constant":true,	
		"inputs":[	
			{	
				"name":"_id",	
				"type":"bytes32"	
			}
		],	
		"name":"relayedBy",	
		"outputs":[	
			{	
				"name":"_relayer",	
				"type":"address"	
			}	
		],	
		"payable":false,	
		"type":"function"	
	}
]
"""
