from telebot import types
import requests
from config import API_KEY
from components.listner.helper import getTokenInfo, formattedPost, getNFTs
from components.listner.networkConfig import NetworkConfig
from components.database import DB

def listener(transactionCount, bot, chat_id, url, contractId, methodId, lastTokenID):
    # get the network from db
    network = DB['group'].find_one({"_id": chat_id})['network']

    # get the network config
    networkConfig = NetworkConfig(network)

    # Make an API call to get the latest minted token
    response = requests.get(f'{networkConfig.api_url}?module=account&action=txlist&address={contractId}&startblock=0&endblock=999999999&sort=asc&apikey=' + networkConfig.get_api_key())

    # Convert the response to JSON
    response = response.json()

    data = sorted(response['result'], key=lambda x: x['timeStamp'], reverse=True)
    data_length = len(data)
    if data_length <= transactionCount:
        if data_length == 10000:
            return (data_length - 100, None)
        return (data_length, None)
    
    # Get hashes of all transactions
    hashes = []
    for i in range(data_length-transactionCount):
        if data[i]['methodId'] == methodId:
            hashes.append(data[i]['hash'])
    
    # Get the from addresses of all transactions
    froms = []
    for i in range(data_length-transactionCount):
        if data[i]['from'] not in froms and data[i]['methodId'] == methodId:
            froms.append(data[i]['from'])
        
    # To get the token ids
    nftsMinted = getNFTs(froms, hashes, contractId, chat_id)
    for nft in nftsMinted:
        if lastTokenID is not None and int(nft["id"]) <= lastTokenID:
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

        # Create the "Mint here!" 
        button = types.InlineKeyboardButton(text="Mint here!", callback_data="mint", url=url)
        markup = types.InlineKeyboardMarkup()
        markup.add(button)

        # Create the formatted message
        if maxSupply == "Infinity":
            caption = formattedPost(nft["id"], nft["from"], totalSupply, "Infinity", nft["timestamp"])
        else:
            caption = formattedPost(nft["id"], nft["from"], maxSupply-totalSupply, maxSupply, nft["timestamp"])

        # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        try:
            bot.send_photo(chat_id=f"{chat_id}", photo=image, caption=caption, reply_markup=markup, parse_mode='HTML')
        except Exception as e:
            print(e)

    if data_length == 10000:
        return (data_length - 100, int(nftsMinted[0]["id"]))

    return (data_length, None)