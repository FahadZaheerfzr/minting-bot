from telebot import TeleBot
from telebot import types
from components.database import DB


def changeContractId(message:types.Message, bot:TeleBot):
    chat_id = message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return
    
    #update the contract id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"contractId": message.text, "lastTransactionCount": None}})
    bot.reply_to(message, "Contract Id updated successfully")


def changeUrl(message, bot):
    chat_id = message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return
    
    #update the url
    DB['group'].update_one({"_id": chat_id}, {"$set": {"url": message.text}})
    bot.reply_to(message, "URL updated successfully")

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

