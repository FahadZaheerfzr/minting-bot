from config import BOT_TOKEN
import telebot
import logging
from components.start import start
from components.listner.listenTransactions import listener
from components.database import DB
from components.listner.helper import getInitialTransactionCount
import time

# Configure logging
logging.basicConfig(filename='transactions.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

mint_bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
me = mint_bot.get_me()
print(me.username)

while True:
    # Find all the groups
    groups = DB['group'].find()
    time.sleep(1)

    # Loop through the groups
    for group in groups:
        # Get the group information
        url = group['url']
        chat_id = group['_id']
        contractId = group['contractId']
        methodId = group['methodId']
        lastTokenID = group['lastTokenID'] if 'lastTokenID' in group and group['lastTokenID'] is not None else None

        if contractId is None or methodId is None:
            continue

        # Get the last transaction count from the database if it exists, else get the initial transaction count from the blockchain
        transactionCount = group['lastTransactionCount'] if 'lastTransactionCount' in group and group['lastTransactionCount'] is not None else getInitialTransactionCount(contractId, chat_id) - 1

        # Call the listener function
        prev_transactionCount = transactionCount  # Store the previous transaction count
        transactionCount, lastTokenID = listener(transactionCount, mint_bot, chat_id, url, contractId, methodId, lastTokenID)

        # Log the transaction information if there is a change
        if transactionCount != prev_transactionCount:
            change = transactionCount - prev_transactionCount
            logging.info(f"Transaction count change for chat ID {chat_id}: {change} (New count: {transactionCount})")
            if lastTokenID is not None:
                logging.info(f"Last token ID for chat ID {chat_id}: {lastTokenID}")

        # Update the last transaction count in the database
        if lastTokenID is not None:
            DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount, "lastTokenID": lastTokenID}})
        else:
            DB['group'].update_one({"_id": chat_id}, {"$set": {"lastTransactionCount": transactionCount}})
