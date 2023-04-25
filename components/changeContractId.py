from telebot import TeleBot
from telebot import types
from components.database import DB

def changeContractId(message, bot):
    chat_id = message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return
    
    #update the contract id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"contractId": message.text}})
    bot.reply_to(message, "Contract Id updated successfully")