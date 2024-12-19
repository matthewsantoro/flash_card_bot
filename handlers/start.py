from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
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

@router.message(Command("add"))
async def add_category_handler(message: Message, command):
    category_name = command.args # Получаем аргументы команды
    if category_name:
        async for session in  db.get_session():
            await db.add_category(session, category_name)
            await message.reply(f"Категория '{category_name}' добавлена.")
    else:
        await message.reply("Пожалуйста, укажите название категории после команды.")
