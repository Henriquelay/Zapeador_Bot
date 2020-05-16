from telegram.ext import Updater
from os import getenv

# CREDENTIALS
token = getenv("token")

# TELEGRAM CONFIG
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
