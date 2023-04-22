from config import RPC_ADDRESS, NFT_ABI
from web3 import Web3
from telebot import types
from telebot import TeleBot


web3 = Web3(Web3.HTTPProvider(RPC_ADDRESS))

def getTokenInfo(tokenAddress,tokenId):
    # Get the token contract
    print(tokenId)
    tokenContract = web3.eth.contract(address=tokenAddress, abi=NFT_ABI)

    #here we are making the function calls, abi has the functions to call for that contract
    allowed = tokenContract.functions.allowedPerBatch().call()
    maxSupply = tokenContract.functions.maxSupply().call()
    tokenURI = tokenContract.functions.tokenURI(tokenId).call()
    totalSupply = tokenContract.functions.totalSupply().call()

    return {
        "allowed": allowed,
        "maxSupply": maxSupply,
        "tokenURI": tokenURI,
        "totalSupply": totalSupply
    }

#we willl use the above function to get the token info

