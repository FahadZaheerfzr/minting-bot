import requests
from config import API_KEY, RPC_ADDRESS, NFT_ABI, ERC_ABI
from web3 import Web3
from datetime import datetime
from components.database import DB
from components.listner.networkConfig import NetworkConfig


def getInitialTransactionCount(contractAddress: str, chat_id: int):
    '''
    This function returns the initial transaction count
    Args:
        contractAddress (str): The contract address

    Returns:
        int: The initial transaction count
    '''

    # Parameters for the API call
    start_block = 0
    end_block = 999999999
    print(chat_id)

    # get the network from db
    network = DB['group'].find_one({"_id": chat_id})['network']

    # get the network config
    networkConfig = NetworkConfig(network)

    # Make an API call to get the latest minted token
    response = requests.get(
        f'{networkConfig.api_url}?module=account&action=txlist&address={contractAddress}&startblock={start_block}&endblock={end_block}&sort=asc&apikey=' + networkConfig.get_api_key())

    # Convert the response to JSON
    response = response.json()

    data_length = len(response['result'])

    print("Initial transaction count: ", data_length)

    return data_length


def getInitialTokenId(contractAddress: str, chat_id: int):
    network = DB['group'].find_one({"_id": chat_id})['network']
    networkConfig = NetworkConfig(network)
    response = requests.get(
        f'{networkConfig.api_url}?module=logs&action=getLogs&fromBlock="latest"&toBlock="latest"&address={contractAddress}&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&apikey=' + networkConfig.get_api_key())

    # Convert the response to JSON
    if response is None:
        return None
    
    response = response.json()
    
    if response['result'] == []:
        return None
    print(response['result'])
    return int(response['result'][-1]['topics'][3], 16)


def getTokenInfo(tokenAddress, tokenId, chat_id):
    '''
    This function returns the token info
    Args:
        tokenAddress (str): The token address
        tokenId (int): The token id

    Returns:
        dict: The token info
    '''
    # get the network from db
    network = DB['group'].find_one({"_id": chat_id})['network']

    # get the network config
    networkConfig = NetworkConfig(network)

    # Create the web3 object
    web3 = Web3(Web3.HTTPProvider(networkConfig.rpc_url))

    # Create the contract object
    tokenContract = web3.eth.contract(address=tokenAddress, abi=NFT_ABI)
    erc_contract = web3.eth.contract(address=tokenAddress, abi=ERC_ABI)

    name = erc_contract.functions.name().call()
    # Get the token info
    try:
        maxSupply = tokenContract.functions.maxSupply().call()
    except:
        maxSupply = "Infinity"

    tokenURI = tokenContract.functions.tokenURI(tokenId).call()
    totalSupply = tokenContract.functions.totalSupply().call()

    # Return the token info
    return {
        "name": name,
        "maxSupply": maxSupply,
        "tokenURI": tokenURI,
        "totalSupply": totalSupply
    }


# def getNFTs(froms, hashes, contractId, chat_id):
#     # get the network from db
#     network = DB['group'].find_one({"_id": chat_id})['network']

#     # get the network config
#     networkConfig = NetworkConfig(network)

#     nftsMinted = []
#     for i in range(len(froms)):
#         transactions = requests.get(
#             f'{networkConfig.api_url}?module=account&action=tokennfttx&contractaddress={contractId}&address={froms[i]}&page=1&offset=100&sort=asc&apikey={networkConfig.get_api_key()}')
#         transactions = transactions.json()
#         if transactions['result']:  # check if 'result' is not empty
#             for tx in sorted(transactions['result'], key=lambda x: x['timeStamp'], reverse=True):
#                 if (tx['hash'] in hashes):
#                     nftsMinted.append(
#                         {
#                             'id': tx['tokenID'],
#                             'from': froms[i],
#                             'timestamp': datetime.fromtimestamp(int(tx['timeStamp']))
#                         }
#                     )
#     nftsMinted.reverse()

#     return nftsMinted


def formattedPost(name, id, from_address, consumed, max, timestamp):
    timeInSeconds = int(timestamp, 16)
    timestampFormatted = datetime.fromtimestamp(timeInSeconds)
    return f"""
    🟩 <b>{name} #{id}</b> has been minted \n
<code>Minter</code>: {from_address}\n
<code>NFTs left</code>: <b> {consumed} / {max}</b>\n
<code>Timestamp</code>: {timestampFormatted} UTC\n
    """
