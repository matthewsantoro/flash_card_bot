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

db = Database(db_config)

async def on_startup(dp):
    await db.connect()
    await db.setup()
    logging.info("Бот запущен и подключен к базе данных.")

async def on_shutdown(dp):
    await db.close()
    logging.info("Бот остановлен и соединение с базой данных закрыто.")



db = Database(db_config)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")




@dp.message(Command("add"))
async def add_category_handler(message: Message, command):
    category_name = command.args # Получаем аргументы команды
    if category_name:
        async for session in  db.get_session():
            await db.add_category(session, category_name)
            await message.reply(f"Категория '{category_name}' добавлена.")
    else:
        await message.reply("Пожалуйста, укажите название категории после команды.")

# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await on_startup(dp)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())