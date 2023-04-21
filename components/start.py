from telebot import types
from telebot import TeleBot

# def start
# This function is called when the user sends the /start command
# It sends a welcome message with an image, a keyboard with three buttons and a "Mint here!" button at the bottom


def start(message, bot):

    # Create the "Mint here!" button
    mint_btn = types.InlineKeyboardButton("Mint here!", callback_data="mint")

    # Create the inline keyboard and add the "Mint here!" button to it
    markup = types.InlineKeyboardMarkup().add(mint_btn)

    # Create the formatted message
    caption = """
🟩 <b>SSSS #130</b> has been minted \n
Minter : <a href="https://t.me/alexnotzank.bnb">@alexnotzank.bnb</a>\n
NFTs left: <b>3290 / 3420</b>\n
Timestamp: Apr-20-2023 06:55:55 PM +UTC\n
<b>Traits:</b>\n
state:       <b>unrevealed</b>\n
"""

    # Send the message with the image and button, and the inline keyboard with the "Mint here!" button
    bot.send_photo(chat_id=message.chat.id, photo=open(r'assets\images\replyImg.jpg', 'rb'),
                   caption=caption, reply_markup=markup, parse_mode='HTML')
