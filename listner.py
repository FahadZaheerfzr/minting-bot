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
    groups = DB['group'].find()
    for group in groups:
        time.sleep(1)
        url = group['url']
        chat_id = group['_id']
        contractId = group['contractId']
        transactionCount = group['lastTransactionCount'] if 'lastTransactionCount' in group else getInitialTransactionCount(contractId) - 1
        transactionCount = listener(transactionCount, mint_bot, chat_id, url, contractId)
        DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount}})

