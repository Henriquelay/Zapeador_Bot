#!/usr/bin/env python3.8

from sys import stdout
from logging import basicConfig as log, DEBUG

from bot_config import dev_chat_id, updater
import bot_functions
import bot_handlers

# Enable logging
FORMAT = '%(asctime)s|[%(levelname)s]%(filename)s/%(funcName)s(): %(message)s'
log(format=FORMAT,
    datefmt='%d/%m/%Y %H:%M:%S',
    level=DEBUG,
    stream=stdout
    )


def main():
    updater.bot.send_message(chat_id=dev_chat_id, text="Liguei caralho💪😎👌", disable_notification=True)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__": 
    main()
