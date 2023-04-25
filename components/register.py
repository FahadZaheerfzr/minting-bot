from telebot import TeleBot
from telebot import types
from components.database import DB

def register(message: types.Message, bot: TeleBot):
    try:
        DB['group'].insert_one({
            "_id": message.chat.id,
            "url": None,
            "contractId": None,
            "owner": message.from_user.id,
            "name": message.chat.title,
        })
        bot.reply_to(message, "Group Registered, Use /settings to manage it")
    except Exception as e:
        bot.reply_to(message, "This community is already registered. Please use /setting to configure your community.")
    