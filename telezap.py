#!/usr/bin/env python3.8

import logging, os
from threading import Thread
from bottle import route, run

from bot_config import dev_chat_id, updater
import bot_handlers

# Enable logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='requests.log',
                    level=logging.DEBUG)


def main():
    updater.start_polling()

    updater.bot.send_message(chat_id=dev_chat_id, text="Liguei caralho💪😎👌", disable_notification=True)

    # Run the bot until Ctrl-C is pressed
    updater.idle()


if __name__ == "__main__": 
    main()
