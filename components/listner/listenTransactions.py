from telebot import types
import requests
from config import API_KEY, NFT_TOKEN_ADDRESS
from components.listner.tokenFunctions import getTokenInfo

def listener(transactionCount, bot):
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
    response = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=txlist&address={NFT_TOKEN_ADDRESS}&startblock={start_block}&endblock={end_block}&sort=asc&apikey=' + API_KEY)

    # Convert the response to JSON
    response = response.json()
    data = sorted(response['result'], key=lambda x: x['timeStamp'], reverse=True)
    data_length = len(data)

    print(type(data_length))
    if data_length <= transactionCount:
        return data_length
    


    #Get Hashes of all transactions
    hashes = []
    for i in range(data_length-transactionCount):
        hashes.append(data[i]['hash'])
    

    # Get the from addresses of all transactions
    froms = []
    for i in range(data_length-transactionCount):
        froms.append(data[i]['from'])
    
    hashes = []
    for i in range(data_length-transactionCount):
        hashes.append(data[i]['hash'])
        
    # To get the token ids
    tokenIDs = []
    for i in range(len(froms)):
        transactions = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=tokennfttx&contractaddress={NFT_TOKEN_ADDRESS}&address={froms[i]}&page=1&offset=100&sort=asc&apikey={API_KEY}')
        transactions = transactions.json()
        if transactions['result']:  # check if 'result' is not empty
            for tx in sorted(transactions['result'], key=lambda x: x['timeStamp'], reverse=True):
                if (tx['hash'] in hashes):
                    tokenIDs.append(tx['tokenID'])

    for ids in tokenIDs:    
        try:
            latestMint = int(tokenIDs[0])
            tokenInfo = getTokenInfo(NFT_TOKEN_ADDRESS, latestMint)
        except:
            print("Error getting token info")

        #return token info allowed, max supply and token uri
        #get image from token uri
        #send the image with the token info
        image = requests.get(tokenInfo['tokenURI']).json()['image']
        maxSupply = tokenInfo['maxSupply']
        totalSupply = tokenInfo['totalSupply']

        # Create the "Mint here!" button
        mint_btn = types.InlineKeyboardButton("Mint here!", callback_data="mint")

        # Create the inline keyboard and add the "Mint here!" button to it
        markup = types.InlineKeyboardMarkup().add(mint_btn)

        # Create the formatted message
        caption = f"""
        🟩 <b>SSSS #{latestMint}</b> has been minted \n
        <code>Minter</code> : <a href="https://t.me/alexnotzank.bnb">@alexnotzank.bnb</a>\n
        <code>NFTs left</code>: <b>{maxSupply-totalSupply} / {maxSupply}</b>\n
        <code>Timestamp</code>: Apr-20-2023 06:55:55 PM +UTC\n
        <b>Traits:</b>\n
        <code>state</code>:       <b>unrevealed</b>\n
        """

    # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
        bot.send_photo(chat_id="1001684016421", photo=image, caption=caption, reply_markup=markup, parse_mode='HTML')
    return data_length