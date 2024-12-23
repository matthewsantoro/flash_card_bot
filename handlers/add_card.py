from aiogram import Router, F
from aiogram.types import Message
from database.db import Database

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(StateFilter(None), Command("add_card"))
async def cmd_add_card(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db = Database()
    sets = await db.get_sets_by_user(user_id)
    await message.answer(
        text="Выберите набор в который вы хотите добавить карточку:",
        #reply_markup=make_row_keyboard(available_food_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(Addcard.choosing_food_name)