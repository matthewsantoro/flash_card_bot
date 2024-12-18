from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from database.db import Database
from bot import db

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Неизвестный"
    async for session in  db.get_session():
        if not await db.user_exists(user_id):
            user = await db.add_user(user_id=user_id, username=username)
            await db.add_set(session, name='Основной набор', creator=user,  )
            await message.reply("Добро пожаловать! Вы были добавлены в базу данных.")
        else:
            await message.reply("Привет снова! Вы уже зарегистрированы.")

