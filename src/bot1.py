from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import logging
import os
from recognizer import *

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Я бот, который умеет распозновать изображения цветов. Жду от тебя фотографию ❤️")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Я жду от тебя фотографию 😄")


def document(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Пришли, пожалуйста, сжатую фотографию 🤨")


def photo(update: Update, context: CallbackContext):
    full_path = None
    prediction = "¯\_(ツ)_/¯"
    try:
        file = context.bot.getFile(update.message.photo[-1].file_id)
        full_path = save_tmp_photo(file.file_path)
        prediction = recognize_flower(full_path)
    except Exception as ex:
        print(ex)
    finally:
        if full_path != None:
            remove_tmp_photo(full_path)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Я думаю, что это {prediction} 😍")


if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.document, document))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo))

    updater.start_polling()
