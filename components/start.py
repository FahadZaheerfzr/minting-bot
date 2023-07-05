from telebot import types


def start(message, bot):
    """
    This function responds to the /start command

    Args:
        message (telebot.types.Message): The message object
        bot (telebot.TeleBot): The bot object
    
    Returns:
        None
    """

    # Create a menu with two buttons: "Register" and "Settings"
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(types.KeyboardButton('/register'), types.KeyboardButton('/settings'))
    # Send the menu to the user
    bot.send_message(message.from_user.id, startFormat(), reply_markup=menu, parse_mode="HTML")

#format for the start command respose message
def startFormat():
    """
    This function returns the format for the /start command response message

    Args:
        None
    """

    return """Hi! I'm <b>RBAmintbot</b>. I respond to the following commands:\n
/register - Register your community\n
/settings - Change your community settings\n
\n<b>Here is how to set me up:</b>\n
1. Use /register to register your community\n
2. Use /settings to change your community settings\n

<b>In settings, you can configure the following:</b>

<b>Change URL</b>: Change the URL of the community.

<b>Change Contract ID</b>: Change the contract ID of the NFT. 
- This is the ID of the NFT contract in the blockchain.

<b>Change Method ID</b>: Change the method ID of the NFT. 
- This is the ID of the method in the NFT contract.

<b>Change Network</b>: Change the network of the community. 
- Currently, the bot supports <b>ETH Mainnet</b>, <b>BSC Mainnet</b>, and <b>BSC Testnet</b>.

<b>NOTE:</b> You can only use /settings if you are the owner of the community.

Please note, I am a beta version. Errors, issues and omissions are possible!\n
<code>Created by @RBAminbot</code>
"""
