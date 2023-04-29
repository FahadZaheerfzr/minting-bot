from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file
from components.listner.listenTransactions import listener
from components.database import DB
from components.listner.helper import getInitialTransactionCount
import time

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username


while True:
    # Find all the groups
    groups = DB['group'].find()

    if len(group) < 4:
        time.sleep(1)
    # Loop through the groups
    for group in groups:
        # Get the group information
        
        url = group['url']
        chat_id = group['_id']
        contractId = group['contractId']
        methodId = group['methodId']
        lastTokenID = group['lastTokenID'] if 'lastTokenID' in group and group['lastTokenID'] is not None else None
        
        if contractId is None or methodId is None or url is None:
            continue
        
        # Get the last transaction count from the database if it exists else get the initial transaction count from the blockchain
        transactionCount = group['lastTransactionCount'] if 'lastTransactionCount' in group and group['lastTransactionCount'] is not None else getInitialTransactionCount(contractId, chat_id) - 5        # Call the listener function
        transactionCount, lastTokenID = listener(transactionCount, mint_bot, chat_id, url, contractId, methodId, lastTokenID)

        # Update the last transaction count in the database
        print("Updating the database with the last transaction count: ", transactionCount)
        print("For the group: ", chat_id)
        if lastTokenID is not None:
            print("Last token id: ", lastTokenID)
            DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount, "lastTokenID": lastTokenID}})
        else:
            DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount}})

