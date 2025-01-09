from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from states.set_state import SetState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard
from aiogram.fsm.context import FSMContext
router = Router()

db = Database()

@router.callback_query(F.data.startswith("set_"), StateFilter(SetState.choose_set))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    pass