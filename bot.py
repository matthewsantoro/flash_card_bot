import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from handlers import start


from database.db import Database

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

# Инициализация базы данных
db_config = {
    'USER': getenv('DB_USER'),
    'PASSWORD': getenv('DB_PASSWORD'),
    'HOST': getenv('DB_HOST'),
    'PORT': getenv('DB_PORT'),
    'DATABASE': getenv('DB_DATABASE')
}



dp = Dispatcher()


async def on_startup(db):
    await db.connect()
    await db.setup()
    logging.info("Бот запущен и подключен к базе данных.")

async def on_shutdown(dp):
    await db.close()
    logging.info("Бот остановлен и соединение с базой данных закрыто.")



db = Database(db_config)






@dp.message(Command("add"))
async def add_category_handler(message: Message, command):
    category_name = command.args # Получаем аргументы команды
    if category_name:
        async for session in  db.get_session():
            await db.add_category(session, category_name)
            await message.reply(f"Категория '{category_name}' добавлена.")
    else:
        await message.reply("Пожалуйста, укажите название категории после команды.")



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start.router)
    await on_startup(db)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())