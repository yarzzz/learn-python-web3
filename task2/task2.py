import sys

from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy

bsc_Urls = [
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.defibit.io/",
    "https://bsc-dataseed1.ninicoin.io/",
    "https://bsc.nodereal.io"
]
bsc = bsc_Urls[0]

VBNB_address = "0xA07c5b74C9B40447a954e1466938b865b6BBea36"

myAddress = "0xC61eb43D6A01a512491Ba08de74dB2D573f56c0b"
myKey = None
if len(sys.argv) > 1:
    myAddress = sys.argv[1]
if len(sys.argv) > 2:
    myKey = sys.argv[2]

def main():
    w3 = Web3(Web3.HTTPProvider(bsc))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

    abi = open("Venus_VBNB.abi").read()

    contractAddress = w3.toChecksumAddress(VBNB_address)
    contract = w3.eth.contract(address=contractAddress, abi=abi)

    # https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction

    logger.debug(w3.eth.get_transaction_count(myAddress))

    def deposit(amount):
        nonce = w3.eth.get_transaction_count(myAddress)
        contract_txn = contract.functions.mint().buildTransaction({
            'value': amount,
            'chainId': 56,
            'gas': 1000000,
            'gasPrice': w3.toWei('5', 'gwei'),
            'nonce': nonce
        })
        recommended_gasPrice = w3.eth.generate_gas_price()
        contract_txn['gasPrice'] = recommended_gasPrice
        logger.debug(contract_txn) # data: 0x1249c58b
        if myKey:
            signed_txn = w3.eth.account.sign_transaction(contract_txn, myKey)
            logger.debug(signed_txn)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.debug(tx_hash)
    
    def withdraw(amount):
        nonce = w3.eth.get_transaction_count(myAddress)
        contract_txn = contract.functions.redeemUnderlying(amount).buildTransaction({
            'value': 0,
            'chainId': 56,
            'gas': 1000000,
            'gasPrice': w3.toWei('5', 'gwei'),
            'nonce': nonce
        })
        recommended_gasPrice = w3.eth.generate_gas_price()
        contract_txn['gasPrice'] = recommended_gasPrice
        logger.debug(contract_txn) # data: 0x852a12e3000000000000000000000000000000000000000000000000016345785d8a0000
        if myKey:
            signed_txn = w3.eth.account.sign_transaction(contract_txn, myKey)
            logger.debug(signed_txn)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.debug(tx_hash)

    amount = 100 * 1000 * 1000 * 1000 * 1000 * 1000
    deposit(amount) # https://bscscan.com/tx/0x39994af0328c3a00c221b229b3cd3c235176f088ed358d3ec8ac3b16092856f8
    withdraw(amount) # https://bscscan.com/tx/0xe99a2d22a6ba09d359a8cee76a31532835b07f8bd3675abafc27ea12edfb313b

if __name__ == '__main__':
    main()
