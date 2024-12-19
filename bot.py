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

from .config import DB_CONFIG, BOT_TOKEN


from database.db import Database

load_dotenv()



dp = Dispatcher()
db = Database(DB_CONFIG)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start.router)
    await db.on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())