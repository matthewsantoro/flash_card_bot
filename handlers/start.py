from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import Database

db = Database()
router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Неизвестный"
    if not await db.get_user_by_id(user_id=user_id):
        await db.add_user(user_id=user_id, name=username)
        user = await db.get_user_by_id(user_id=user_id)
        await db.add_deck(name="Основной набор", creator_id=user.id)
        await message.reply("Добро пожаловать! Вы были добавлены в базу данных.")
    else:
        await message.reply("Привет снова! Вы уже зарегистрированы.")



