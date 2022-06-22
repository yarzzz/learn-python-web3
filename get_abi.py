import json

import requests

def get_abi(contractAddress):
    apiUrl = "https://api.bscscan.com/api"
    apiEndpoint = apiUrl+"?module=contract&action=getabi&address=" + str(contractAddress)

    r = requests.get(url = apiEndpoint)
    abi = r.json()["result"]
    f = open("tmp.abi", "w")
    f.write(abi)
    f.close()

if __name__ == '__main__':
    get_abi("0xA07c5b74C9B40447a954e1466938b865b6BBea36")
