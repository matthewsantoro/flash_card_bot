import asyncio
import logging
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import start, add_card, main_menu, set, cards

from config import BOT_TOKEN
from database.db import Database

load_dotenv()

async def main() -> None:
    dp = Dispatcher()
    db = Database()
    await db.setup()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start.router,main_menu.router,add_card.router,set.router, cards.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())