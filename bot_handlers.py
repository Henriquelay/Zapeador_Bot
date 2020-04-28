from telegram.ext import CommandHandler, Filters, MessageHandler, InlineQueryHandler

from bot_config import dispatcher
import bot_functions


# Initialize handlers
start_handler = CommandHandler('start', bot_functions.command_start)
help_handler = CommandHandler(('help', 'ajuda'), bot_functions.command_help)
zapear_handler = CommandHandler('zapear', bot_functions.command_zapear)
vtfgoverno_handler = CommandHandler(('vtfgoverno', '600conto'), bot_functions.vtfgoverno)

zapear_message_handler = MessageHandler(Filters.text, bot_functions.zapear_if_private)

zapear_inline_handler = InlineQueryHandler(bot_functions.inlinequery)

# Add handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(zapear_handler)
dispatcher.add_handler(zapear_inline_handler)
dispatcher.add_handler(vtfgoverno_handler)

dispatcher.add_error_handler(bot_functions.error)
dispatcher.add_handler(zapear_message_handler)

