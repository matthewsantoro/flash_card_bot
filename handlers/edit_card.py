
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db import Database
from states.cards import CardState
from aiogram.types import Message, CallbackQuery
from keyboards.cards import create_edit_card_keyboard


router = Router()

db = Database()

@router.callback_query(F.data.startswith("card_edit:"),StateFilter(CardState.view_card))
async def choosing_edit(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    data = await state.get_data()
    cards = data["cards"]
    card = cards[index]
    text = f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}\n\nВыберете, что именно вы хотите изменить"
    keyboard = create_edit_card_keyboard(card_id=card.id)
    callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_"),StateFilter(CardState.view_card))
async def editing_card(callback: CallbackQuery, state: FSMContext):
    card_id = int(callback.data.split(":")[1])
    state.update_data(edit_card_id=card_id)
    if 'front' in callback.data:
        text='Введите передню часть карточки'
        state.set_state(CardState.edit_front)
    else:
        text = 'Введите заднюю часть карточки'
        state.set_state(CardState.edit_back)
    callback.message.answer(text=text)

@router.callback_query(StateFilter(CardState.edit_back,CardState.edit_front))
async def front_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    card_id = data['edit_card_id']
    if state.get_state() == CardState.edit_front:
        db.

    



