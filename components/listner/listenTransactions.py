from telebot import types
import requests
from config import API_KEY
from components.listner.helper import getTokenInfo, formattedPost, getNFTs

def listener(transactionCount, bot, chat_id, url, contractId, methodId):
    '''
    This function listens to the transactions

    Args:
        bot (telebot.TeleBot): The bot object
    
    Returns:
        None
    '''
    
    # Make an API call to get the latest minted token
    response = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=txlist&address={contractId}&startblock=0&endblock=999999999&sort=asc&apikey=' + API_KEY)

    # Convert the response to JSON
    response = response.json()


    data = sorted(response['result'], key=lambda x: x['timeStamp'], reverse=True)
    data_length = len(data)
    if data_length <= transactionCount:
        return data_length
    

    #Get Hashes of all transactions
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
    nftsMinted = getNFTs(froms, hashes, contractId)
    
    for nft in nftsMinted:
        try:
            tokenInfo = getTokenInfo(contractId, int(nft["id"]))
        except Exception as e:
            print(e)
            continue
        #return token info allowed, max supply and token uri
        #get image from token uri
        #send the image with the token info
        try:
            image = requests.get(tokenInfo['tokenURI']).json()['image']
        except:
            image = requests.get(tokenInfo['tokenURI']+".jpg").content

        maxSupply = tokenInfo['maxSupply']
        totalSupply = tokenInfo['totalSupply']

        # Create the "Mint here!" button
        mint_btn = types.InlineKeyboardButton(text="Mint here!", url=url)

        # Create the inline keyboard and add the "Mint here!" button to it
        markup = types.InlineKeyboardMarkup().add(mint_btn)

        # Create the formatted message
        if maxSupply == "Infinity":
            caption = formattedPost(nft["id"], nft["from"], totalSupply, "Infinity", nft["timestamp"])
        else:
            caption = formattedPost(nft["id"], nft["from"], maxSupply-totalSupply, maxSupply, nft["timestamp"])

    # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        bot.send_photo(chat_id=f"{chat_id}", photo=image, caption=caption, reply_markup=markup, parse_mode='HTML')
    return data_length