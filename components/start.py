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
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton("Register", callback_data="register"))
    menu.add(types.InlineKeyboardButton("Settings", callback_data="settings"))
    # Send the menu to the user
    bot.send_message(message.from_user.id, startFormat(), reply_markup=menu, parse_mode="HTML")

#format for the start command respose message
def startFormat():
    """
    This function returns the format for the /start command response message

    Args:
        None
    """

    return """
Hi! I'm <b>RBAmintbot</b>. Let's get started: \n

<b>Here's how to set me up:</b> \n
Add me to your community and make me an admin. \n
Send the command /register in your community. \n
Send the command /settings to me to set up your mint bot. \n

<b>In settings, you can configure the following: </b> \n
<b>Change URL</b>: Update the community URL. \n
<b>Change Contract ID</b>: Modify the NFT contract ID in the blockchain. \n
<b>Change Network</b>: Switch between ETH Mainnet, BSC Mainnet, and BSC Testnet. \n

<b>NOTE:</b> You can only use /settings if you are the owner of the community. \n

Please note, I am in beta version, so errors, issues, and omissions are possible! \n

<code>Created by @Roburna </code>
"""
