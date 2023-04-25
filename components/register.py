from telebot import TeleBot
from telebot import types


def register(message: types.Message, bot: TeleBot):
    try:
        bot.reply_to(message, "Group Registered, Use /help to manage it")
        return message.chat.id
    except:
        bot.reply_to(message, "This community is already registered. Please use /setting to configure your community.")
    