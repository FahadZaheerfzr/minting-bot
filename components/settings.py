from telebot import TeleBot
from telebot import types
from components.database import DB


def setContract(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    #update the contract id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"contractId": message.text, "lastTransactionCount": None}})
    bot.reply_to(message, "Contract ID updated successfully", reply_markup=types.ReplyKeyboardRemove())


def changeContractId(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message, bot)
    
    #update the contract id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id,
                        "Please enter your contract id.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setContract, bot, chat_id)



def setUrl(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled",  reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    #update the url
    DB['group'].update_one({"_id": chat_id}, {"$set": {"url": message.text}})
    bot.reply_to(message, "Url updated successfully",  reply_markup=types.ReplyKeyboardRemove())


def changeUrl(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message, bot)
    
    #update the url
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id,
                        "Please enter your url.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setUrl, bot, chat_id)
    

def setMethodId(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    #update the method id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"methodId": message.text}})
    bot.reply_to(message, "Method ID updated successfully", reply_markup=types.ReplyKeyboardRemove())


def changeMethodId(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message, bot)
    
    #update the method id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id,
                        "Please enter your method id.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setMethodId, bot, chat_id)


def settings(message, bot):
    chat_id = message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return
    
    #Give buttons to change the settings
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Change URL", callback_data="changeUrl"))
    markup.add(types.InlineKeyboardButton(text="Change Contract Id", callback_data="changeContractId"))
    markup.add(types.InlineKeyboardButton(text="Change Method Id", callback_data="changeMethodId"))
    bot.reply_to(message, "Please select the setting you want to change", reply_markup=markup)