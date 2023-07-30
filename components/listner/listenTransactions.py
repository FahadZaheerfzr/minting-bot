from telebot import types
import requests
from config import API_KEY
from components.listner.helper import getTokenInfo, formattedPost
from components.listner.networkConfig import NetworkConfig
from components.database import DB
import logging

# Configure logging
logging.basicConfig(filename='message.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def listener(bot, chat_id, url, contractId, methodId, lastTokenID):
    # get the network from db
    network = DB['group'].find_one({"_id": chat_id})['network']
    # get the network config
    networkConfig = NetworkConfig(network)

    

    # Make an API call to get the latest minted token
    response = requests.get(
        f'{networkConfig.api_url}?module=logs&action=getLogs&fromBlock="latest"&toBlock="latest"&address={contractId}&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&apikey=' + networkConfig.get_api_key())
    

    if not response:
        return (lastTokenID)
    
    intTokenId = lastTokenID
    response = response.json()

    if (response['status'] == '0'):
        return (lastTokenID)

    # sort the response
    originalLength = len(response['result'])
    reversed_response = response['result'][::-1]

    latestTokenId = int(reversed_response[0]['topics'][3],16)


    if (latestTokenId - intTokenId) == 0:
        return (lastTokenID)
    
    reversed_response = reversed_response[:latestTokenId - intTokenId]
    # now reverse it again
    reversed_response = reversed_response[::-1]

    # we will loop as many as the difference and get token info for each new token

    for i in range(latestTokenId - intTokenId):
        # get the token id
        
        tokenId = reversed_response[i]['topics'][3]
        # get the token info
        tokenInfo = getTokenInfo(contractId, int(tokenId,16), chat_id)

        if tokenInfo is None:
            continue
        # get the token image
        try:
            image = requests.get(tokenInfo['tokenURI']).json()['image']
        except:
            image = requests.get(tokenInfo['tokenURI']+".jpg").content

        maxSupply = tokenInfo['maxSupply']
        totalSupply = tokenInfo['totalSupply']
        name = tokenInfo['name']

        # Create the "Mint here!"
        button = types.InlineKeyboardButton(
            text="Mint here!", callback_data="mint", url=url)
        markup = types.InlineKeyboardMarkup()
        markup.add(button)

        # Create the formatted message
        if maxSupply == "Infinity":
            caption = formattedPost(
                name, int(tokenId,16), reversed_response[i]['address'], totalSupply, "Infinity", reversed_response[i]['timeStamp'])
        else:
            caption = formattedPost(
                name,int(tokenId,16), reversed_response[i]['address'], maxSupply-totalSupply, maxSupply, reversed_response[i]['timeStamp'])

        # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        try:
            message = bot.send_photo(chat_id=f"{chat_id}", photo=image,
                                    caption=caption, reply_markup=markup, parse_mode='HTML')
            message_id = message.message_id
            logging.info(f"Message ID for chat ID {chat_id} and token ID {tokenId}: {message_id},name:{name},from:{reversed_response[i]['address']}")
        except Exception as e:
            logging.error(f"Error sending message for chat ID {chat_id} and token ID {tokenId}: {e}")
    return latestTokenId
    


