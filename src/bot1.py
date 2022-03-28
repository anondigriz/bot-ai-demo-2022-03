from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import logging
import os
# from recognizer import *

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Я бот, который умеет распозновать изображения цветов. Жду от тебя фотографию ❤️")


if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
