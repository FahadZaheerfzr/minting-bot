from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file
from components.register import register #import the register function from the register.py file
from components.settings import settings #import the settings function from the settings.py file
from components.database import DB

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

#message handler for the /start command
mint_bot.register_message_handler(start, pass_bot=True, commands=['start'])
mint_bot.register_message_handler(register, pass_bot=True, commands=['register'])
mint_bot.register_message_handler(settings, pass_bot=True, commands=['settings'])

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username
mint_bot.polling() #start the bot