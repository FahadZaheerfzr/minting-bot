import logging
from telebot import TeleBot
from telebot import types
from components.database import DB

# Configure logging
logging.basicConfig(filename='settings.log', level=logging.INFO)

# Create a TeleBot instance
bot = TeleBot('your_token_here')

def setContract(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    # Update the contract id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"contractId": message.text, "lastTransactionCount": None}})
    bot.reply_to(message, "Contract ID updated successfully", reply_markup=types.ReplyKeyboardRemove())

    # Log the setting change
    logging.info(f"Contract ID updated: Chat ID={chat_id}, New Contract ID={message.text}")


def changeContractId(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message.message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message.message, bot)
    
    # Update the contract id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id, "Please enter your contract id.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setContract, bot, chat_id)
    logging.info(f"User requested to change Contract ID: Chat ID={chat_id}")


def setUrl(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled",  reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    # Update the URL
    DB['group'].update_one({"_id": chat_id}, {"$set": {"url": message.text}})
    bot.reply_to(message, "URL updated successfully",  reply_markup=types.ReplyKeyboardRemove())

    # Log the setting change
    logging.info(f"URL updated: Chat ID={chat_id}, New URL={message.text}")


def changeUrl(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message.message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message.message, bot)
    
    # Update the URL
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id, "Please enter your URL.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setUrl, bot, chat_id)
    logging.info(f"User requested to change URL: Chat ID={chat_id}")


def setMethodId(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    # Update the method id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"methodId": message.text}})
    bot.reply_to(message, "Method ID updated successfully", reply_markup=types.ReplyKeyboardRemove())

    # Log the setting change
    logging.info(f"Method ID updated: Chat ID={chat_id}, New Method ID={message.text}")


def changeMethodId(message:types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    groupInfo = DB['group'].find_one({"_id": chat_id})

    if groupInfo is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return settings(message.message, bot)
    
    if groupInfo['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return settings(message.message, bot)
    
    # Update the method id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id, "Please enter your method id.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setMethodId, bot, chat_id)
    logging.info(f"User requested to change Method ID: Chat ID={chat_id}")


def changeNetwork(message: types.CallbackQuery, bot):
    chat_id = message.message.chat.id
    group_info = DB['group'].find_one({"_id": chat_id})

    if group_info is None:
        bot.answer_callback_query(message.id, text="This community is not registered. Please use /register to register your community.")
        return

    if group_info['owner'] != message.from_user.id:
        bot.answer_callback_query(message.id, text="You are not the owner of this community.")
        return

    # Create the inline keyboard for network selection
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton("ETH Mainnet", callback_data="network_eth_mainnet"),
               types.InlineKeyboardButton("BSC Mainnet", callback_data="network_bsc_mainnet"),
               types.InlineKeyboardButton("BSC Testnet", callback_data="network_bsc_testnet"))
    
    bot.send_message(message.from_user.id, "Please select the network you want to use.", reply_markup=markup)
    bot.register_next_step_handler(message.message, setNetwork, bot)
    logging.info(f"User requested to change Network: Chat ID={chat_id}")


def setNetwork(message, bot):
    chat_id = message.chat.id
    group_info = DB['group'].find_one({"_id": chat_id})

    if group_info is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return

    if group_info['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return

    if message.text == "ETH Mainnet":
        DB['group'].update_one({"_id": chat_id}, {"$set": {"network": "eth_mainnet"}})
        bot.reply_to(message, "Network updated successfully", reply_markup=types.ReplyKeyboardRemove())
        logging.info(f"Network updated: Chat ID={chat_id}, New Network=ETH Mainnet")
    elif message.text == "BSC Mainnet":
        DB['group'].update_one({"_id": chat_id}, {"$set": {"network": "bsc_mainnet"}})
        bot.reply_to(message, "Network updated successfully", reply_markup=types.ReplyKeyboardRemove())
        logging.info(f"Network updated: Chat ID={chat_id}, New Network=BSC Mainnet")
    elif message.text == "BSC Testnet":
        DB['group'].update_one({"_id": chat_id}, {"$set": {"network": "bsc_testnet"}})
        bot.reply_to(message, "Network updated successfully", reply_markup=types.ReplyKeyboardRemove())
        logging.info(f"Network updated: Chat ID={chat_id}, New Network=BSC Testnet")
    else:
        bot.reply_to(message, "Invalid network selected", reply_markup=types.ReplyKeyboardRemove())
        logging.warning(f"Invalid network selected: Chat ID={chat_id}")


def settings(message, bot):
    chat_id = message.chat.id
    group_info = DB['group'].find_one({"_id": chat_id})

    if group_info is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return

    if group_info['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return

    # Create the inline keyboard for settings selection
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Change URL", callback_data="changeUrl"))
    markup.add(types.InlineKeyboardButton("Change Contract Id", callback_data="changeContractId"))
    markup.add(types.InlineKeyboardButton("Change Method Id", callback_data="changeMethodId"))
    markup.add(types.InlineKeyboardButton("Change Network", callback_data="changeNetwork"))

    bot.send_message(message.from_user.id, settingFormat(), reply_markup=markup, parse_mode="HTML")

    logging.info(f"User accessed settings: Chat ID={chat_id}")

def settingFormat():
    return """
<b>Please select the setting you want to change:</b>
"""
