from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file
from components.register import register #import the register function from the register.py file
from components.settings import settings, changeContractId, changeMethodId, changeUrl, changeNetwork,handleSelectedCommunity,cancel,removeCommunity, cancel_callback #import the settings function from the settings.py file
from components.database import DB

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

#message handler for the /start command
mint_bot.register_message_handler(start, pass_bot=True, commands=['start'])
mint_bot.register_message_handler(register, pass_bot=True, commands=['register'])
mint_bot.register_message_handler(settings, pass_bot=True, commands=['settings'])
mint_bot.register_message_handler(cancel, pass_bot=True, commands=['cancel'])

mint_bot.register_callback_query_handler(handleSelectedCommunity, pass_bot=True, func=lambda call: call.data.startswith('handleSelectedCommunity|'))
mint_bot.register_callback_query_handler(changeUrl, pass_bot=True, func=lambda call: call.data.startswith('changeUrl_'))
mint_bot.register_callback_query_handler(changeContractId, pass_bot=True, func=lambda call: call.data.startswith('changeContractId_'))
mint_bot.register_callback_query_handler(changeMethodId, pass_bot=True, func=lambda call: call.data.startswith('changeMethodId_'))
mint_bot.register_callback_query_handler(changeNetwork, pass_bot=True, func=lambda call: call.data.startswith('changeNetwork_'))
mint_bot.register_callback_query_handler(removeCommunity, pass_bot=True, func=lambda call: call.data.startswith('removeCommunity_'))
mint_bot.register_callback_query_handler(cancel_callback, pass_bot=True, func=lambda call: call.data.startswith('cancel_'))

me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username
mint_bot.polling() #start the bot