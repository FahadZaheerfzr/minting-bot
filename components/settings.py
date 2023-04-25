from telebot import TeleBot
from telebot import types
from components.database import DB
from components.changeUrl import changeUrl
from components.changeContractId import changeContractId

def settings(message, bot):
    chat_id = message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return
    
    #allow user to change the url
    if message.text == "/settings":
        bot.reply_to(message, "Please enter the new url ")
        bot.register_next_step_handler(message, changeUrl, bot)

    #allow user to change the contract id
    elif message.text == "/settings contract":
        bot.reply_to(message, "Please enter the new contract id below")
        bot.register_next_step_handler(message, changeContractId, bot)

