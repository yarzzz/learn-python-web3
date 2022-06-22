import time
import requests
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from web3 import Web3

bsc_Urls = [
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.defibit.io/",
    "https://bsc-dataseed1.ninicoin.io/",
    "https://bsc.nodereal.io"
]
bsc = bsc_Urls[3]

pancakeSwapAddress = "0x10ed43c718714eb63d5aa57b78b54704e256024e"
pancakeSwapFactoryAddress = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"

def main():
    w3 = Web3(Web3.HTTPProvider(bsc))
    # logger.debug(w3.isConnected())

    abi = open("PancakeSwap_factory.abi").read()
    # logger.debug(abi)

    contractAddress = w3.toChecksumAddress(pancakeSwapFactoryAddress)
    contract = w3.eth.contract(address=contractAddress, abi=abi)

    allPairsLength = contract.functions.allPairsLength().call()
    logger.debug(allPairsLength)

    allPairs = ["" for _ in range(allPairsLength)]

    def getPairByIndex(index):
        while True:
            try:
                allPairs[index] = contract.functions.allPairs(index).call()
                logger.debug("%s %s" % (index, allPairs[index]))
                return
            except requests.exceptions.ProxyError as e:
                logger.warning(f"ProxyError: {index}")
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"ConnectionError: {index}")
            except Exception as e:
                # TODO {'code': -32603, 'message': 'internal error'}
                logger.error(f"{index} Other Error: [{type(e)}] {e}")
                return
            time.sleep(1)

    # rate limit of bsc endpoint refers to: https://docs.bnbchain.org/docs/rpc#rate-limit
    curIndex = 0
    limit_rate = {"count": 10, "interval": 1}

    # for i in range(allPairsLength):
    #     getPairByIndex(i)
    while curIndex < allPairsLength:
        logger.info(curIndex)

        sleepUntilTime = time.time() + limit_rate["interval"]
        with ThreadPoolExecutor(4) as executor:
            executor.map(getPairByIndex, [index for index in range(curIndex, min(curIndex + limit_rate["count"], allPairsLength))])
        f = open("pancakeSwapAddresses.txt", "a")
        for address in allPairs[curIndex:curIndex+limit_rate["count"]]:
            f.write(address)
            f.write("\n")
        f.close()
        curIndex += limit_rate["count"]
        sleepTime = sleepUntilTime - time.time()
        if sleepTime > 0:
            time.sleep(sleepTime)
    logger.info("finish")

if __name__ == '__main__':
    main()
