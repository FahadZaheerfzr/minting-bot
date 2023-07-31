import logging
from telebot import TeleBot
from telebot import types
from components.database import DB
import re

# Configure logging
logging.basicConfig(filename='settings.log', level=logging.INFO)

# Create a TeleBot instance
bot = TeleBot('your_token_here')

def setContract(message, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    # Update the contract id
    DB['group'].update_one({"_id": chat_id}, {"$set": {"contractId": message.text, "lastTokenID": None}})
    bot.reply_to(message, "Contract ID updated successfully. Please update the network accordingly", reply_markup=types.ReplyKeyboardRemove())

    # Log the setting change
    logging.info(f"Contract ID updated: Chat ID={chat_id}, New Contract ID={message.text}")

def changeContractId(message:types.CallbackQuery, bot):
    data = message.data.split("_")
    chat_id = data[1]
    #to int
    chat_id = int(chat_id)

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

def setUrl(message:types.CallbackQuery, bot, chat_id):
    if message.text == "cancel":
        bot.reply_to(message, "Cancelled", reply_markup=types.ReplyKeyboardRemove())
        return settings(message, bot)

    url = message.text.strip()

    # URL validation check
    if not is_valid_url(url):
        bot.reply_to(message, "Invalid URL format. Please enter a proper URL.")
        bot.register_next_step_handler(message, setUrl, bot, chat_id)
        return

    # Update the URL
    DB['group'].update_one({"_id": chat_id}, {"$set": {"url": url}})
    bot.reply_to(message, "URL updated successfully", reply_markup=types.ReplyKeyboardRemove())

    # Log the setting change
    logging.info(f"URL updated: Chat ID={chat_id}, New URL={url}")


def changeUrl(message: types.CallbackQuery, bot):
    #get callback data
    data = message.data.split("_")
    chat_id = data[1]
    #to int
    chat_id = int(chat_id)
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


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)



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
    data = message.data.split("_")
    chat_id = data[1]
    #to int
    chat_id = int(chat_id)
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
    data = message.data.split("_")
    chat_id = data[1]
    #to int
    chat_id = int(chat_id)
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
    bot.register_next_step_handler(message.message, setNetwork, bot, chat_id)
    logging.info(f"User requested to change Network: Chat ID={chat_id}")


def setNetwork(message, bot, chat_id):
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


def manageCommunity(message, bot,selectedCommunity):
    chat_id = message.from_user.id
    # selectedCommunity = selectedCommunity.split(" ")[-1][1:-1]
    logging.info(f"Manage community: Chat ID={chat_id}, Community ID={selectedCommunity}")
    selectedCommunity=float(selectedCommunity)
    group_info = DB['group'].find_one({"_id": int(selectedCommunity)})

    if group_info is None:
        bot.reply_to(message, "This community is not registered. Please use /register to register your community.")
        return

    if group_info['owner'] != message.from_user.id:
        bot.reply_to(message, "You are not the owner of this community.")
        return


    # Create the inline keyboard for settings selection
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Change URL", callback_data="changeUrl_" + str(group_info['_id'])))
    markup.add(types.InlineKeyboardButton("Change Contract Id", callback_data="changeContractId_" + str(group_info['_id'])))
    #markup.add(types.InlineKeyboardButton("Change Method Id", callback_data="changeMethodId_" + str(group_info['_id'])))
    markup.add(types.InlineKeyboardButton("Change Network", callback_data="changeNetwork_" + str(group_info['_id'])))
    markup.add(types.InlineKeyboardButton("Remove this community", callback_data="removeCommunity_" + str(group_info['_id'])))

    bot.send_message(message.from_user.id, settingFormat(), reply_markup=markup, parse_mode="HTML")

    logging.info(f"User accessed settings for community: Chat ID={chat_id}, Community ID={group_info['_id']}")

def removeCommunity(message, bot):
    data = message.data.split("_")
    chat_id = data[1]
    #to int
    chat_id = int(chat_id)
    group_info = DB['group'].find_one({"_id": chat_id})

    if group_info is None:
        bot.send_message(message.from_user.id, "This community is not registered. Please use /register to register your community.")
        return

    if group_info['owner'] != message.from_user.id:
        bot.send_message(message.from_user.id, "You are not the owner of this community.")
        return

    DB['group'].delete_one({"_id": chat_id})
    bot.send_message(message.from_user.id, "Community removed successfully", reply_markup=types.ReplyKeyboardRemove())
    logging.info(f"Community removed: Chat ID={chat_id}, Community ID={group_info['_id']}")

def settings(message, bot):
    chat_id = message.chat.id
    groups = DB['group'].find({"owner": message.from_user.id})

    if len(list(groups.clone())) == 0:
        bot.reply_to(message, "You are not the owner of any community.")
        return

    communities = []
    for group in groups:
        community_name = group["name"]
        community_id = group["_id"]
        community_info = f"{community_name} ({community_id})"
        communities.append(community_info)
        

    reply_text = "List of owned communities:\n\n"
    for idx, community in enumerate(communities, 1):
        reply_text += f"{idx}. {community}\n"
    logging.info(f"User Communities: Chat ID={chat_id}, Communities={communities}")

    reply_text += "\nPlease select a community by entering its corresponding number or type 'cancel' to exit."
    markup = types.InlineKeyboardMarkup()
    for idx in range(1, len(communities) + 1):
        markup.add(types.InlineKeyboardButton(str(communities[idx - 1]), callback_data="handleSelectedCommunity|" + str(communities[idx - 1])))


    markup.add(types.InlineKeyboardButton("cancel", callback_data="handleSelectedCommunity_cancel"))

    # Store the selected community in selectedCommunity
    selectedCommunity = None


    bot.send_message(message.from_user.id, settingFormatCommunity(), reply_markup=markup, parse_mode="HTML")
    # bot.register_next_step_handler(message, handleSelectedCommunity)

def handleSelectedCommunity(message: types.CallbackQuery,bot):
    data = message.data.split("|")
    logging.info(f"User selected data: data={data}")
    selectedCommunity = data[1].split(" ")[-1][1:-1]
    if selectedCommunity == 'ance':
        bot.send_message(message.from_user.id, "Action canceled.")
        return 

    try:
        logging.info(f"handleSelectedCommunity:Community ID={selectedCommunity}")
        manageCommunity(message, bot, selectedCommunity)

    except ValueError:
        bot.send_message(message.from_user.id, "Invalid input. Please try again.")

def cancel(message, bot):
    bot.send_message(message.from_user.id, "Action canceled.")
    return

def settingFormat():
    return """
<b> Please select the option you wish to change:</b>
"""


def settingFormatCommunity():
    return """
<b> Please select the community you wish to set up the mintbot:</b>
"""
