from logging import getLogger, DEBUG
from requests import post as postrequest
from argparse import ArgumentParser, ArgumentError
from json import loads as jsonloads

from uuid import uuid4
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, constants
from telegram.utils.helpers import escape_markdown

from utils import bot_utils, bot_messages

functionsLogger = getLogger(__name__)
functionsLogger.setLevel(DEBUG)

@run_async
def zapear_if_private(update, context):
    """Zapirotalha o texto se chat privado"""

    functionsLogger.debug("Entering zapear_if_private")

    if(update.message.chat.type) == 'private':
        command_zapear(update, context)

    functionsLogger.debug("Exiting zapear_if_private")


@run_async
@bot_utils.send_typing_action
def command_zapear(update, context):
    """Zapironeia o texto mandado por mensagem privada ou comando"""


    functionsLogger.debug("Entering zapear")
    try:
        response = zapear(update.message.text)
    except bot_utils.emptyMessageException:
        functionsLogger.debug("Exception caught! emptyMessageException")
        response = bot_messages.emptyMessage
    except bot_utils.flagWithoutValueException:
        functionsLogger.debug("Exception caught! flagWithoutValueException")
        response = bot_messages.argumentError

    finally:
        if response.__len__() > constants.MAX_MESSAGE_LENGTH:
            response = bot_messages.messageSizeError
        context.bot.send_message(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, text=response)
    
    functionsLogger.debug("Exiting zapear")

@run_async
@bot_utils.send_typing_action
def command_help(update, context):
    """Send help message to user"""

    functionsLogger.debug("Entering help")

    context.bot.send_message(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.helpMessage, parse_mode="MarkdownV2", disable_web_page_preview=True)

    functionsLogger.debug("Exiting help")

@run_async
@bot_utils.send_typing_action
def command_start(update, context):
    """Send the start message to user"""

    functionsLogger.debug("Entering start")

    context.bot.send_message(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, text=bot_messages.welcomeMessage, parse_mode="MarkdownV2", disable_web_page_preview=True)

    functionsLogger.debug("Exiting start")

@run_async
def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    if query != '':
        moods = ["angry", "sassy", "sick", "happy", "sad"]
        moodsEmoji = ["😤", "😏", "🤒", "😁", "😭"]

        results = [
                    InlineQueryResultArticle(
                    id=uuid4(),
                    title=moodsEmoji[moodIndex] + " " + mood.capitalize(),
                    input_message_content=InputTextMessageContent(
                        zapear((query + " -mood " + mood))
                    ))
                for moodIndex, mood in enumerate(moods)]

        update.inline_query.answer(results)
    else:
        update.inline_query.answer([])



###########

def zapear(msg):
    """Zapiroza o texto enviado"""

    functionsLogger.debug("Entering zapear")

    parsed_args = parse_flags(msg)

    if not parsed_args:
        print("PARSE RETORNEI PARADA ESTRANHA")

    parsed_dict = vars(parsed_args)
    functionsLogger.debug("Parsed dict:")
    functionsLogger.debug(parsed_dict)

    if not parsed_dict['zap']:
        functionsLogger.debug("'" + msg + "' is empty of actual text. Raising exception...")
        raise bot_utils.emptyMessageException(msg)

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

    msg = msg.split(' ') 

    if(msg[0][0] == '/'):
        msg = msg[1:]


    functionsLogger.debug("Parsing: '" + ' '.join(msg) + "'")

    parser = bot_utils.ThrowingArgumentParser(prog='Zapeador')

    parser.add_argument('-str', nargs=1, required=False, type=int, choices=range(1,6), default=3)
    parser.add_argument('-rate', nargs=1, required=False, type=float, default=1)
    parser.add_argument('-tweet', nargs=1, required=False, type=bool, default=False)
    parser.add_argument('-mood', nargs=1, required=False, choices=["angry", "happy", "sad", "sassy", "sick"],  default='angry')
    parser.add_argument('zap', nargs='*')

    argv = parser.parse_args(msg)

    functionsLogger.debug("Exiting flag parse")
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
    apiURL = 'http://vemdezap.herokuapp.com/api/v1.0/zap'
    response = postrequest(apiURL, data=dict)

    if(response == None):
        functionsLogger.error(f"Could not get response from {apiURL}")
    else:
        functionsLogger.debug(f"API respose was: {response.content}")

    functionsLogger.debug("Exiting api_call")
    return jsonloads(response.content)['zap']


@run_async
def error(update, context):
    """Log errors caused by Updates."""

    functionsLogger.warning('Update %s caused error "%s"', update.update_id, context.error)
    return
