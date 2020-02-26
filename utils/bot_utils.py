import logging
from functools import wraps
import telegram

import sys
sys.path.append(sys.path[0] + "/..")

utilsLogger = logging.getLogger(__name__)
utilsLogger.setLevel(logging.DEBUG)


# Decorators to simulate user feedback
def send_action(action):
    """Send `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func

    return decorator


send_typing_action = send_action(telegram.ChatAction.TYPING)
send_upload_photo_action = send_action(telegram.ChatAction.UPLOAD_PHOTO)
send_upload_video_action = send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_document_action = send_action(telegram.ChatAction.UPLOAD_DOCUMENT)


def parse_n_images_input(update, context, text):
    """Parse input for VPR gifs. Input must exist and be numeric.
    Returns
    --------
    (nImages, nImagesMessage)
    nImages : int
        Number of images to be fetched.
    nImagesMessage : str
        Message to be sent by the bot.
    """
