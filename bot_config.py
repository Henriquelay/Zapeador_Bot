import os
import telegram
from telegram.ext import Updater

# CREDENTIALS
token = os.environ.get("TELEGRAM_TELEZAP_TOKEN")
dev_chat_id = os.environ.get("DEV_CHAT_ID")

# TELEGRAM CONFIG
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
bot = telegram.Bot(token)
