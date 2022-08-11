import constants
from requests import get
from matplotlib import pyplot as plt
from datetime import datetime

def make_api_url(module, action, address, **kwargs):
    url = constants.BASE_URL + f"?module={module}&action={action}&address={address}&apikey={constants.API_KEY}"
    print(url)
    for key, value in kwargs.items():
        url+= f"&{key}={value}"
    
    return url

def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()
    value = int(data["result"])/ constants.ETHER_VALUE
    return value

def get_transactions(address):
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=1000, sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offser=1000,sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    current_balance = 0
    balances = [] 
    times = []

    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / constants.ETHER_VALUE

        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / constants.ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / constants.ETHER_VALUE
        
        time = datetime.fromtimestamp(int(tx['timeStamp']))
        
        if to.lower() == address.lower():
            current_balance += value
        else:
            current_balance -= value + gas
        balances.append(current_balance)
        times.append(time)
    

   # print("Here "  + str(len(times)) + " ," + str(len(balances)))
    plt.plot(times, balances)
    plt.show()

address = "0x73bceb1cd57c711feac4224d062b0f6ff338501e"

get_transactions(address)
get_transactions('0x0716a17FBAeE714f1E6aB0f9d59edbC5f09815C0')