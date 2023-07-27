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
            "methodId": "0xa0712d68",
            "network": "bsc_testnet",
        })
        bot.reply_to(message, "Group registered, use the command /settings in my dm to manage your mintbot")
    except Exception as e:
        bot.reply_to(message, "This community is already registered. Please use /settings in my dm to configure your community.")
    