from telebot import types
from telebot import TeleBot


# def start 
# This function is called when the user sends the /start command
# It sends a simple welcome message and a keyboard with two buttons

def start(message, bot):
    bot.reply_to(message, "Welcome to the bot!") #send a welcome message as reply to the message

    
