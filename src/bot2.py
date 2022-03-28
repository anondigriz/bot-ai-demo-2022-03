import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from recognizer import *

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ умный бот с AI\nЯ основан на aiogram.")


@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    full_path = get_path_for_saving()
    await message.photo[-1].download(destination_file=full_path)
    prediction = recognize_flower(full_path)

    with open(full_path, 'rb') as photo:
        await message.reply_photo(photo, caption=f'Тут {prediction} 💐')
    remove_tmp_photo(full_path)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я жду от тебя фотографию 😄")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
