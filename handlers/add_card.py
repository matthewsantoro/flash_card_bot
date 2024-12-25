from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from states.add_card_state import AddCard
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard

router = Router()

@router.message(StateFilter(None), Command("add_card"))
async def cmd_add_card(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db = Database()
    sets = await db.get_sets_by_user_id(user_id)
    keyboard = await create_sets_keyboard(sets=sets)
    await message.answer(
        text="Выберите набор в который вы хотите добавить карточку:",
        reply_markup=keyboard
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(AddCard.choose_set)


@router.callback_query(F.data.startswith("set_") ,StateFilter(AddCard.choose_set))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    set_id = int(callback.data.split("_")[1])
    if set_id == 0:
       await callback.message.answer(
        text="Введите название набора:"
        )
       await state.set_state(AddCard.add_set)
    else: 
       await state.update_data(set_id=set_id)
       await state.set_state(AddCard.enter_question)

@router.message(StateFilter(AddCard.add_set))
async def add_set(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db = Database()
    new_set = await db.add_set(creator_id=user_id, name=message.text)
    await message.reply(f"Набор '{new_set.name}' добавлен.")
    await state.update_data(set_id=new_set.id)
    await state.set_state(AddCard.enter_question)

    

    
       
       