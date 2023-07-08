import logging
import datetime
import connect
from aiogram import Bot, Dispatcher, executor, types
API = "6312267659:AAHDbFXldMS3_Q2Wo3a4Ao3JusqTF62LyZs" # токен бота

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API)
dp = Dispatcher(bot)

# Создание таблицы пользователей телеграмм
try:
    with connect.connection.cursor() as cursor:
        cursor.execute("CREATE TABLE `telegram`(id INT(11), name VARCHAR(32), time_request DATETIME, url_account VARCHAR(32),premium VARCHAR(32), usernm VARCHAR(32), PRIMARY KEY(id)")
except Exception as ex:
    print(ex)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Hello')

@dp.message_handler(commands=['info'])
async def info(msg: types.Message):
    await msg.answer(f"User_id: {msg.from_user.id}\n"
                     f"Name: {msg.from_user.full_name}\n"
                     f"Datetime: {datetime.datetime.now()}\n"
                     f"URL: {msg.from_user.url}\n"
                     f"Premium: {msg.from_user.is_premium}\n"
                     f"Username: @{msg.from_user.username}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)