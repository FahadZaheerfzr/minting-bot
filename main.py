from config import BOT_TOKEN 
import telebot # pip install pyTelegramBotAPI
from components.start import start #import the start function from the start.py file

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # create a bot object with the bot token we have

#message handlers
mint_bot.register_message_handler(start, pass_bot=True, commands=["start"]) #register the start function to the /start command we are passing the bot object and a function to check if the message is a command



me = mint_bot.get_me() #get the bot information
print(me.username) #print the bot username
print("Bot is running...")
#set bot to listen to commands
mint_bot.polling()