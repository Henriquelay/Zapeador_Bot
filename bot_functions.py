from logging import getLogger, DEBUG
from requests import post as postrequest
from argparse import ArgumentParser, REMAINDER
from json import loads as jsonloads

from telegram.ext.dispatcher import run_async

from utils import bot_utils, bot_messages

functionsLogger = getLogger(__name__)
functionsLogger.setLevel(DEBUG)

# @run_async
def zapear_if_private(update, context):
    """Zapirotalha o texto se chat privado"""

    print("\n\nFodase CATCH ALL\n\n")

    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=update.message.text)

    if update.message.chat.username == None:
        user = '@' + update.message.chat.first_name
    else:
        user = update.message.chat.username

    chat_type = update.message.chat.type
    
    functionsLogger.debug(f"Catch all: {chat_type} to {user}")

    if(chat_type) == 'private':
        command_zapear(update, context)


# @run_async
# @bot_utils.send_typing_action
def command_zapear(update, context):
    """Zapironeia o texto mandado por mensagem privada ou comando"""

    print("\n\nFodase CMD_ZAP\n\n")

    message = update.message.text.split(' ')
    if message[0][0] == '/':
        response = zapear(message[1:], update)
    else:
        response = zapear(message, update)

    if response != None:
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=response)

# @run_async
# @bot_utils.send_typing_action
def command_help(update, context):
    """Send help message to user"""

    print("\n\nFodase CMD_HELP\n\n")

    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.helpMessage, parse_mode="markdown", disable_web_page_preview=True)

# @run_async
# @bot_utils.send_typing_action
def command_start(update, context):
    """Send the start message to user"""

    print("\n\nFodase CMD_START\n\n")

    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.welcomeMessage, parse_mode="markdown")


def zapear(msg, update):
    """Zapiroza o texto enviado"""

    functionsLogger.debug("Entering zapear")
    
    parsed_args = parse_flags(msg)
    if not parsed_args:
        return
    parsed_dict = vars(parsed_args)
    if not parsed_dict['zap']:
        return

    functionsLogger.debug("Exiting zapear")
    return api_call(**parsed_dict)


def parse_flags(msg):
    '''
    Parses the flags of sent messages.
    Input is a list of strings of the text message
    Flags:
    -mood: ["angry", "happy", "sad", "sassy", "sick"]
    -str: strength [1..5]
    -rate: float 0..1 # Check API for details : https://github.com/vmarchesin/vemdezapbe.be
    -tweet: boolean

    Return the arguments in a list (and on for the remainder of the message, named 'zap')
    '''

    functionsLogger.debug("Initiating flag parse")

    parser = ArgumentParser(prog='Zapeador')
    parser.add_argument('-str', nargs=1, required=False, type=int, choices=range(1,6), default=3)
    parser.add_argument('-rate', nargs=1, required=False, type=float, default=0.5)
    parser.add_argument('-tweet', nargs=1, required=False, type=bool, default=False)
    parser.add_argument('-mood', nargs=1, choices=["angry", "happy", "sad", "sassy", "sick"], required=False, default='happy')
    parser.add_argument('zap', nargs=REMAINDER)
    try:
        argv = parser.parse_args(msg)
    except:
        return
    functionsLogger.debug("Initiating flag parse complete")
    return argv


def api_call(str, rate, tweet, mood, zap):
    '''
    Access the API and return the response text
    '''

    functionsLogger.debug("Entering api_call")

    dict = {
        'zap':' '.join(zap),    # Contatenates the list of string return in ['zap']
        'mood':mood,
        'strength':str,
        'rate':rate,
        'tweet':tweet
        }
    apiURL = 'http://vemdezapbe.be/api/v1.0/zap'
    response = postrequest(apiURL, data=dict)

    if(response == None):
        functionsLogger.error(f"Could not get response from {apiURL}")
    else:
        functionsLogger.debug(f"API respose was: {response}")

    functionsLogger.debug("Exiting api_call")
    return jsonloads(response.content)['zap']


# @run_async
def error(update, context):
    """Log errors caused by Updates."""

    functionsLogger.warning('Update %s caused error "%s"', update.update_id, context.error)
    return
