from config import BOT_TOKEN
import telebot
import logging
from components.start import start
from components.listner.listenTransactions import listener
from components.database import DB
from components.listner.helper import getInitialTransactionCount, getInitialTokenId
import time

# Configure logging
logging.basicConfig(filename='transactions.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
me = mint_bot.get_me()
print(me.username)

while True:
    # Find all the groups
    groups = DB['group'].find()
    time.sleep(1)

    # Loop through the groups
    for group in groups:
        # Get the group information
        url = group['url']
        chat_id = group['_id']
        contractId = group['contractId']
        methodId = group['methodId']
        lastTokenID = group['lastTokenID'] if 'lastTokenID' in group and group['lastTokenID'] is not None else None
        if contractId is None or methodId is None:
            continue
        if group["name"] is not None:
            print(group["name"] + " has " + str(group["lastTokenID"]) + " token ID")

        # Get the last transaction count from the database if it exists, else get the initial transaction count from the blockchain
        if lastTokenID is not None:
            lastTokenID = group['lastTokenID']
            
        else:
            lastTokenID = getInitialTokenId(contractId, chat_id) - 2
        
        
        # Call the listener function
        lastTokenID = listener(mint_bot, chat_id, url, contractId, methodId, lastTokenID)
        
        
        # Update the last transaction count in the database
        if lastTokenID is not None:
            DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTokenID": lastTokenID}})
