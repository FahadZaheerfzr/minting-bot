from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
import time
from components.start import start #import the start function from the start.py file

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

#global num_transactions
num_transactions = 0
# define a function to check for new transactions
def check_transactions():
    global num_transactions # use the global keyword to access the global variable
    num_transactions=start(mint_bot,num_transactions)
    # update the last number of transactions for future checks

# initialize the last number of transactions to 0

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username
print("Bot is running...")

# run the check_transactions function in a while loop
while True:
    time.sleep(5)
    check_transactions()