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


# taking the url, contractId and _id from group with name "farad and lars" abhi kai liyai, later will get all, abhi cant see what array i get cuz cant run
group = DB['group'].find_one({"name": "farad and lars"})
#the url
url = group['url']
chat_id = group['_id']
contractId = group['contractId']

transactionCount = getInitialTransactionCount(contractAddress=contractId) - 1


while True:
    time.sleep(5)
    print("Listening...")
    transactionCount = listener(transactionCount, mint_bot, chat_id, url, contractId)
