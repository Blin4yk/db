import logging
import connect
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import results
from random import randint as r
from time import sleep as t

API = "6312267659:AAHDbFXldMS3_Q2Wo3a4Ao3JusqTF62LyZs" # токен бота

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API)
dp = Dispatcher(bot)

buttons = ["Лидеры","Испытать удачу","Магазин","Тап ₽"]
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

callback_kb = types.InlineKeyboardMarkup()
callback_kb.add(types.InlineKeyboardButton(text="Лидеры", callback_data="leaders"))

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
        value = r(0,1001)
        unlucky_value = open('img/photo_2023-07-10_19-54-11.jpg', 'rb')
        lucky_value = open('C:\pythonProject2\img\pixil-frame-0 (4).png', 'rb')

        if value < 1000:
            results.Money(msg.from_user.id, 1)
            await bot.send_photo(msg.chat.id, unlucky_value, caption=f'В сундуке {results.balance(msg.from_user.id)} монет', reply_markup=callback_kb)

        else:
            results.Money(msg.from_user.id, value * 10)
            await bot.send_photo(msg.chat.id, lucky_value, caption=f'О повезло повезло начислено {value*10}, в сундуке {results.balance(msg.from_user.id)} монет')
    elif msg.text == "Лидеры":
        pass

@dp.callback_query_handler(text="leaders")
async def leader(cbq: CallbackQuery):
    await bot.answer_callback_query(cbq.id, text=f"{results.leaders(cbq.from_user.id)}", show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






