#!/usr/bin/env python3.8

from logging import basicConfig as log, DEBUG

from bot_config import dev_chat_id, updater

# Enable logging
log(format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='requests.log',
    level=DEBUG)


def main():
    updater.start_polling()

    updater.bot.send_message(chat_id=dev_chat_id, text="Liguei caralho💪😎👌", disable_notification=True)

    # Run the bot until Ctrl-C is pressed
    updater.idle()


if __name__ == "__main__": 
    main()
