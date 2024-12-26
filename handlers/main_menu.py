from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from states.add_card_state import AddCard
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from utils.text import MAIN_MENU_TEXT
from keyboards.menu import create_main_menu

router = Router()

@router.message(Command('menu'))  # [2]
async def main_menu(message: Message):
    keyboard = await create_main_menu()
    await message.answer(text=MAIN_MENU_TEXT, reply_markup=keyboard)
    