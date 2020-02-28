from functools import wraps
from telegram import ChatAction


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


send_typing_action = send_action(ChatAction.TYPING)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_document_action = send_action(ChatAction.UPLOAD_DOCUMENT)
