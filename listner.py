from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file
from components.listner.listenTransactions import listener
import time
mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username




transactionCount = 9

while True:
    time.sleep(5)
    print("Listening...")
    transactionCount = listener(transactionCount, mint_bot)
