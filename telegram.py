import logging
import datetime
import connect
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import config

API = "6312267659:AAHDbFXldMS3_Q2Wo3a4Ao3JusqTF62LyZs" # токен бота

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API)
dp = Dispatcher(bot)

# Приветствие
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    try:
        with connect.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO `gamers`(name, premium, username, id_user) VALUES ('{msg.from_user.first_name}',"
                           f"'{msg.from_user.is_premium}',"
                           f"'{msg.from_user.username}',"
                           f"{msg.from_user.id})")
            connect.connection.commit()
    except Exception as ex:
        print(ex)

    finally:
        connect.connection.cursor().close()
    await msg.answer('Привет, это игра монетка, чем больше тапаешь, тем больше монеток зарабатываешь', reply_markup=kb)


@dp.message_handler()
async def tap(msg: types.Message):
    if msg.text == "Тап ₽":
        config.count += 1
        await msg.answer(f"Кол-во: {config.count}")


tap_keyboard = KeyboardButton("Тап ₽")
kb = ReplyKeyboardMarkup()
kb.add(tap_keyboard)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






