from telebot import types
from telebot import TeleBot
from web3 import Web3
import requests
from config import API_KEY, NFT_TOKEN_ADDRESS
from components.tokenFunctions import getTokenInfo

def start(message, bot):
    # Make an API call
    #get the token info



    response = requests.get('https://api-testnet.bscscan.com/api?module=account&action=txlist&address=0xC0f1182bB2bAF816177E09bDf909AC62201D8230&startblock=1&endblock=99999999&sort=asc&apikey=' + API_KEY)

    response = response.json()
    #here we will get the token info


    #get hashes of all transactions
    hashes = []
    for i in range(len(response['result'])):
        hashes.append(response['result'][i]['hash'])
    

    #also the from addresses
    froms = []
    for i in range(len(response['result'])):
        froms.append(response['result'][i]['from'])
    
    hashes = []
    for i in range(len(response['result'])):
        hashes.append(response['result'][i]['hash'])
        
    #to get the token ids
    tokenIDs = []
    for i in range(len(froms)):
        transactions = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=tokennfttx&contractaddress={NFT_TOKEN_ADDRESS}&address={froms[i]}&page=1&offset=100&sort=asc&apikey={API_KEY}')
        transactions = transactions.json()
        if transactions['result']:  # check if 'result' is not empty
            for tx in sorted(transactions['result'], key=lambda x: x['timeStamp'], reverse=True):
                tokenIDs.append(tx['tokenID'])

    latestMint = int(tokenIDs[0])
    tokenInfo = getTokenInfo(NFT_TOKEN_ADDRESS, latestMint)
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
🟩 <b>SSSS #130</b> has been minted \n
<code>Minter</code> : <a href="https://t.me/alexnotzank.bnb">@alexnotzank.bnb</a>\n
<code>NFTs left</code>: <b>{-totalSupply+maxSupply} / {maxSupply}</b>\n
<code>Timestamp</code>: Apr-20-2023 06:55:55 PM +UTC\n
<b>Traits:</b>\n
<code>state</code>:       <b>unrevealed</b>\n
"""

    # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
    bot.send_photo(chat_id=message.chat.id, photo=image, caption=caption, reply_markup=markup, parse_mode='HTML')
