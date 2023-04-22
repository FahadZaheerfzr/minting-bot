from config import RPC_ADDRESS, NFT_ABI
from web3 import Web3
from telebot import types
from telebot import TeleBot


web3 = Web3(Web3.HTTPProvider(RPC_ADDRESS))

def getTokenInfo(tokenAddress,tokenId=1):
    # Get the token contract
    tokenContract = web3.eth.contract(address=tokenAddress, abi=NFT_ABI)

    #here we are making the function calls, abi has the functions to call for that contract
    allowed = tokenContract.functions.allowedPerBatch().call()
    maxSupply = tokenContract.functions.maxSupply().call()
    tokenURI = tokenContract.functions.tokenURI(tokenId).call()

    return {
        "allowed": allowed,
        "maxSupply": maxSupply,
        "tokenURI": tokenURI
    }

#we willl use the above function to get the token info

