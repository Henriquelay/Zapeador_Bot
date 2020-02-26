from telegram import Bot
from telegram.ext import Updater
from dotenv import load_dotenv
from os import getenv

# CREDENTIALS
load_dotenv()
token = getenv("token")
dev_chat_id = getenv("dev_chat_id")

# TELEGRAM CONFIG
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(token)
