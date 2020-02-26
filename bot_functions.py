from logging import getLogger, DEBUG
from requests import post as postrequest
from argparse import ArgumentParser, REMAINDER
from json import loads as jsonloads

from telegram.ext.dispatcher import run_async

from utils import bot_utils, bot_messages

functionsLogger = getLogger(__name__)
functionsLogger.setLevel(DEBUG)

@run_async
def zapear_if_private(update, context):
    """Zapirotalha o texto se chat privado"""

    functionsLogger.debug(f"MessageHandler: {update.message.chat} : {update.message.text}")

    if(update.message.chat.type) == 'private':
        command_zapear(update, context)
    return


@bot_utils.send_typing_action
@run_async
def command_zapear(update, context):
    """Zapironeia o texto mandado por mensagem privada ou comando"""
    
    message = update.message.text.split(' ')
    if message[0][0] == '/':
        response = zapear(message[1:], update)
    else:
        response = zapear(message, update)

    if response == None:
        functionsLogger.debug(f"⮑ Channel {update.message.chat.username}  [{update.message.chat.id}]:  ({response})")
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.noText)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=response)
        functionsLogger.debug(f"⮑ {update.message.chat.first_name} {update.message.chat.last_name} [{update.message.chat.id}]:  ({response})")
    return

@run_async
@bot_utils.send_typing_action
def command_help(update, context):
    """Send help message to user"""

    functionsLogger.debug(f"{update.message.chat.type} to @{update.message.chat.username}")

    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.helpMessage, parse_mode="markdown", disable_web_page_preview=True)
    return


@bot_utils.send_typing_action
def command_start(update, context):
    """Send the start message to user"""

    functionsLogger.debug(f"{update.message.chat.type} to @{update.message.chat.username}")

    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.welcomeMessage, parse_mode="markdown")
    return


def zapear(msg, update):
    """Zapiroza o texto enviado"""

    functionsLogger.debug(f"{update.message.chat.type} to @{update.message.chat.username}")
    
    parsed_args = parse_flags(msg)
    if not parsed_args:
        return
    parsed_dict = vars(parsed_args)
    if not parsed_dict['zap']:
        return
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
    # print(vars(argv)['zap'])
    return argv


def api_call(str, rate, tweet, mood, zap):
    '''
    Access the API and return the response text
    '''
    dict = {
        'zap':' '.join(zap),    # Contatenates the list of string return in ['zap']
        'mood':mood,
        'strength':str,
        'rate':rate,
        'tweet':tweet
        }
    # print(dict)
    response = postrequest('http://vemdezapbe.be/api/v1.0/zap', data=dict)
    return jsonloads(response.content)['zap']


@run_async
def error(update, context):
    """Log errors caused by Updates."""

    functionsLogger.warning('Update %s caused error "%s"', update.update_id, context.error)
    return
