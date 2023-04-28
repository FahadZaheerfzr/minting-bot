from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file
from components.listner.listenTransactions import listener
from components.database import DB
import time
from components.listner.helper import getInitialTransactionCount

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username


while True:
    # Find all the groups
    groups = DB['group'].find()
    # Loop through the groups
    for group in groups:
        # Sleep for 1 second
        time.sleep(1)
        # Get the group information
        url = group['url']
        chat_id = group['_id']
        contractId = group['contractId']
        methodId = group['methodId']
        
        # Get the last transaction count from the database if it exists else get the initial transaction count from the blockchain
        transactionCount = group['lastTransactionCount'] if 'lastTransactionCount' in group else getInitialTransactionCount(contractId, chat_id) - 5

        # Call the listener function
        transactionCount = listener(transactionCount, mint_bot, chat_id, url, contractId, methodId)

        # Update the last transaction count in the database
        DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount}})

