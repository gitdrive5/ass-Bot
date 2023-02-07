import os
import logging
import telegram
from telegram import InputFile
from telegram.ext import Updater, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Your bot's token, obtained from BotFather
BOT_TOKEN = os.environ.get("TOKEN", "")

# Channel where logs will be sent
LOG_CHANNEL = -1001836419410  # Replace with the id of the channel

def send_to_log_channel(bot, update):
    message = update.message
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    text = f"Message from {username} ({first_name} {last_name})\n"
    text += f"Chat ID: {chat_id}\n"
    text += f"User ID: {user_id}\n"
    text += f"Message Text: {message.text}\n"

    # Send the message text to the log channel
    bot.send_message(chat_id=LOG_CHANNEL, text=text)

    # Send media files to the log channel
    for file in message.photo or message.document or message.audio or message.voice or message.video:
        bot.send_document(chat_id=LOG_CHANNEL, document=InputFile(file.file_id))

def error(bot, update, error):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add a handler to handle messages
    dp.add_handler(MessageHandler(Filters.all, send_to_log_channel))

    # Add an error handler
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
