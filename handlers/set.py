from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from states.add_card_state import AddCard
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard
from aiogram.fsm.context import FSMContext
router = Router()

db = Database()


@router.callback_query(F.data =="menu_set")
async def get_sets_card(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    sets = await db.get_sets_by_user_id(user_id)
    await state.update_data(msg_id=callback.message.message_id)
    keyboard = await create_sets_keyboard(sets=sets)
    await callback.message.edit_text(
        text="Выберите коллекцию:",
        reply_markup=keyboard,
    )
    await state.set_state(AddCard.choose_set)


@router.callback_query(F.data =="menu_addcard")
async def cmd_add_card(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    sets = await db.get_sets_by_user_id(user_id)
    await state.update_data(msg_id=callback.message.message_id)
    keyboard = await create_sets_keyboard(sets=sets)
    await callback.message.edit_text(
        text="Выберите коллекцию в которую вы хотите добавить карточку:",
        reply_markup=keyboard,
    )
    await state.set_state(AddCard.choose_set)