from telebot import types
import requests
from config import API_KEY
from components.listner.tokenFunctions import getTokenInfo
from datetime import datetime

def listener(transactionCount, bot, chat_id, url, contractId):
    '''
    This function listens to the transactions

    Args:
        bot (telebot.TeleBot): The bot object
    
    Returns:
        None
    '''


    # Parameters for the API call
    start_block = 0
    end_block = 999999999
    
    # Make an API call to get the latest minted token
    response = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=txlist&address={contractId}&startblock={start_block}&endblock={end_block}&sort=asc&apikey=' + API_KEY)

    # Convert the response to JSON
    response = response.json()


    data = sorted(response['result'], key=lambda x: x['timeStamp'], reverse=True)
    data_length = len(data)

    if data_length <= transactionCount:
        return data_length
    


    #Get Hashes of all transactions
    hashes = []
    for i in range(data_length-transactionCount):
        if data[i]['methodId'] == "0xa0712d68":
            hashes.append(data[i]['hash'])
    

    # Get the from addresses of all transactions
    froms = []
    for i in range(data_length-transactionCount):
        if data[i]['from'] not in froms and data[i]['methodId'] == "0xa0712d68":
            froms.append(data[i]['from'])
        
    # To get the token ids
    nftsMinted = []
    for i in range(len(froms)):
        transactions = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=tokennfttx&contractaddress={contractId}&address={froms[i]}&page=1&offset=100&sort=asc&apikey={API_KEY}')
        transactions = transactions.json()
        if transactions['result']:  # check if 'result' is not empty
            for tx in sorted(transactions['result'], key=lambda x: x['timeStamp'], reverse=True):
                if (tx['hash'] in hashes):
                    nftsMinted.append(
                        {
                            'id': tx['tokenID'],
                            'from': froms[i],
                            'timestamp': datetime.fromtimestamp(int(tx['timeStamp']))
                        }
                    )
    nftsMinted.reverse()
    for nft in nftsMinted:
        try:
            tokenInfo = getTokenInfo(contractId, int(nft["id"]))
        except:
            print("Token not found")
            continue
        #return token info allowed, max supply and token uri
        #get image from token uri
        #send the image with the token info
        image = requests.get(tokenInfo['tokenURI']).json()['image']
        maxSupply = tokenInfo['maxSupply']
        totalSupply = tokenInfo['totalSupply']

        # Create the "Mint here!" button
        mint_btn = types.InlineKeyboardButton(f"<a href='{url}'>Mint here!</a>", callback_data="mint")

        # Create the inline keyboard and add the "Mint here!" button to it
        markup = types.InlineKeyboardMarkup().add(mint_btn)

        # Create the formatted message
        caption = f"""
        🟩 <b>SSSS #{nft["id"]}</b> has been minted \n
<code>Minter</code> : {nft["from"]}\n
<code>NFTs left</code>: <b>{maxSupply-totalSupply} / {maxSupply}</b>\n
<code>Timestamp</code>: {nft["timestamp"]} +UTC\n
        """

    # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        bot.send_photo(chat_id=f"{chat_id}", photo=image, caption=caption, reply_markup=markup, parse_mode='HTML')
    return data_length