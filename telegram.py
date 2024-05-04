import logging

import aiogram.dispatcher.filters.state

import connect
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import results
from random import randint as r
from time import sleep as t
from aiogram.dispatcher.filters.state import State, StatesGroup
API = "Token"  # токен бота

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API)
dp = Dispatcher(bot)

# Кнопки
buttons = ["Испытать удачу", "Магазин", "Тап ₽"]
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

# CallBack кнопки
callback_kb = InlineKeyboardMarkup()
callback_kb.add(InlineKeyboardButton(text="Лидеры", callback_data="leaders"))
# callback_kb.add(types.InlineKeyboardButton(text="Испытать удачу", callback_data="lucky_game"))

callback_lucky = InlineKeyboardMarkup()
callback_lucky.add(InlineKeyboardButton(text="Испытать удачу", callback_data="lucky_game"))

# Приветствие
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    try:
        with connect.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO `gamers`(name, premium, username, id_user) VALUES "
                           f"('{msg.from_user.first_name}',"
                           f"'{msg.from_user.is_premium}',"
                           f"'{msg.from_user.username}',"
                           f"{msg.from_user.id})")
            connect.connection.commit()
    except Exception as ex:
        print(ex)

    finally:
        connect.connection.cursor().close()
    await msg.answer('Привет, это игра монетка, чем больше тапаешь, тем больше монеток зарабатываешь', reply_markup=kb)

# Создаем класс состояний
class States(StatesGroup):
    waiting_for_message = State()

@dp.message_handler()
async def tap(msg: types.Message):
    if msg.text == "Тап ₽":
        value = r(0,1001)
        unlucky_value = open('img/photo_2023-07-10_19-54-11.jpg', 'rb')
        lucky_value = open('img/pixil-frame-0 (4).png', 'rb')
        treasure = open('img/pixil-frame-0 (5).png', 'rb')

        if value < 980 and value != 777:
            results.Money(msg.from_user.id, 1, "coin")
            await bot.send_photo(msg.chat.id, unlucky_value,
                                 caption=f'В сундуке {results.balance(msg.from_user.id)} монет',
                                 reply_markup=callback_kb)
        elif value == 777:
            results.Money(msg.from_user.id, 1, "treasure")
            await bot.send_photo(msg.chat.id, treasure,
                                 caption=f'В сундуке {results.balance(msg.from_user.id)} монет',
                                 reply_markup=callback_kb)
        else:
            results.Money(msg.from_user.id, value * 10, "diam")
            await bot.send_photo(msg.chat.id, lucky_value,
                                 caption=f'О повезло повезло начислено {10000}, в сундуке '
                                         f'{results.balance(msg.from_user.id)} монет',
                                 reply_markup=callback_kb)

    elif msg.text == "Испытать удачу":
        await msg.answer(f"Баланс {results.balance(msg.from_user.id)}", reply_markup=callback_lucky)

@dp.callback_query_handler(text="leaders")
async def leader(cbq: CallbackQuery):
    await bot.answer_callback_query(cbq.id, text=f"{results.leaders(cbq.from_user.id)}", show_alert=True)

@dp.callback_query_handler(text="lucky_game")
async def leader(cbq: CallbackQuery):
    await cbq.answer("Какую сумму вы хотите поставить?")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






