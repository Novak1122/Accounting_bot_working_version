
from aiogram import executor
from db import botdb
from dispatcher import dp
from handlers import personal_actions

botdb = botdb('bot_database.db')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
