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
    try:
        with connect.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO `ttt`(id, name, url_account, premium, usernm) VALUES ({msg.from_user.id},{msg.from_user.first_name},'{msg.from_user.url}','{msg.from_user.is_premium}','{msg.from_user.username}');")
            connect.connection.commit()
    except Exception as ex:
        print(ex)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)