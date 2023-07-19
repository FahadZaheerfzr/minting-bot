from telebot import types
import requests
from config import API_KEY
from components.listner.helper import getTokenInfo, formattedPost, getNFTs
from components.listner.networkConfig import NetworkConfig
from components.database import DB
import logging

# Configure logging
logging.basicConfig(filename='message.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def listener(transactionCount, bot, chat_id, url, contractId, methodId, lastTokenID):
    # get the network from db
    print("The transaction count is: ", transactionCount)
    network = DB['group'].find_one({"_id": chat_id})['network']

    # get the network config
    networkConfig = NetworkConfig(network)

    # Make an API call to get the latest minted token
    response = requests.get(
        f'{networkConfig.api_url}?module=account&action=txlist&address={contractId}&startblock=0&endblock=999999999&sort=asc&apikey=' + networkConfig.get_api_key())

    # Convert the response to JSON
    if not response:
        return (transactionCount, None)

    response = response.json()

    if response is not None:
        data = response.get('result')
        if data is not None:
            data = sorted(data, key=lambda x: x['timeStamp'], reverse=True)
    else:
        return (transactionCount, None)
    
    logging.info(f"The data length for chat ID {chat_id} is {len(data)}")
    data_length = len(data)
    if data_length <= transactionCount:
        if data_length == 10000:
            logging.warning(f"Transaction count for chat ID {chat_id} is 10000. This is the maximum number of transactions that can be fetched from the API. The last transaction count will be set to 9900.")
            return (data_length - 100, None)
        return (data_length, None)

    hashes = []
    for i in range(data_length-transactionCount):
        if i < data_length and data[i]['methodId'] == methodId:
            hashes.append(data[i]['hash'])

    # Get the from addresses of all transactions
    froms = []
    for i in range(data_length-transactionCount):
        if i < data_length and data[i]['methodId'] == methodId:
            if data[i]['from'] not in froms:
                froms.append(data[i]['from'])

    # To get the token ids
    nftsMinted = getNFTs(froms, hashes, contractId, chat_id)
    for nft in nftsMinted:
        if lastTokenID is not None and int(nft["id"]) <= lastTokenID:
            print (f"Token ID {nft['id']} has already been processed for chat ID {chat_id}.")
            logging.info(f"Token ID {nft['id']} has already been processed for chat ID {chat_id}.")
            return

        try:
            tokenInfo = getTokenInfo(contractId, int(nft["id"]), chat_id)
        except Exception as e:
            print(e)
            continue

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
                name, nft["id"], nft["from"], totalSupply, "Infinity", nft["timestamp"])
        else:
            caption = formattedPost(
                name, nft["id"], nft["from"], maxSupply-totalSupply, maxSupply, nft["timestamp"])

        # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        try:
            message = bot.send_photo(chat_id=f"{chat_id}", photo=image,
                                     caption=caption, reply_markup=markup, parse_mode='HTML')
            message_id = message.message_id
            logging.info(f"Message ID for chat ID {chat_id} and token ID {nft['id']}: {message_id},name:{name},from:{nft['from']}")
        except Exception as e:
            print(e)

    if data_length == 10000:
        logging.warning(f"Transaction count for chat ID {chat_id} is 10000. This is the maximum number of transactions that can be fetched from the API. The last transaction count will be set to 9900.")
        return (data_length - 100, int(nftsMinted[0]["id"]))

    return (data_length, None)
