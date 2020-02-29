#!/usr/bin/env python3.8

from sys import stdout
from logging import basicConfig as log, DEBUG

from telegram.ext import CommandHandler, Filters, MessageHandler

from bot_config import dev_chat_id, updater, dispatcher
import bot_functions

# Enable logging
FORMAT = '%(asctime)s|[%(levelname)s]%(filename)s/%(funcName)s(): %(message)s'
log(format=FORMAT,
    datefmt='%d/%m/%Y %H:%M:%S',
    level=DEBUG,
    stream=stdout
    )

# Initialize handlers
start_handler = CommandHandler('start', bot_functions.command_start)
help_handler = CommandHandler(('help', 'ajuda'), bot_functions.command_help)
zapear_handler = CommandHandler('zapear', bot_functions.command_zapear)
zapear_message_handler = MessageHandler(Filters.text, bot_functions.zapear_if_private)

# Add handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(zapear_handler)
dispatcher.add_error_handler(bot_functions.error)
dispatcher.add_handler(zapear_message_handler)



def main():
    updater.bot.send_message(chat_id=dev_chat_id, text="Liguei caralho💪😎👌", disable_notification=True)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__": 
    main()
