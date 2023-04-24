from config import RPC_ADDRESS, NFT_ABI
from web3 import Web3


# Create the web3 object
web3 = Web3(Web3.HTTPProvider(RPC_ADDRESS))

def getTokenInfo(tokenAddress,tokenId):
    '''
    This function returns the token info
    Args:
        tokenAddress (str): The token address
        tokenId (int): The token id
    
    Returns:
        dict: The token info
    '''

    # Create the contract object
    tokenContract = web3.eth.contract(address=tokenAddress, abi=NFT_ABI)
    
    # Get the token info
    allowed = tokenContract.functions.allowedPerBatch().call()
    maxSupply = tokenContract.functions.maxSupply().call()
    tokenURI = tokenContract.functions.tokenURI(tokenId).call()
    totalSupply = tokenContract.functions.totalSupply().call()

    # Return the token info
    return {
        "allowed": allowed,
        "maxSupply": maxSupply,
        "tokenURI": tokenURI,
        "totalSupply": totalSupply
    }


