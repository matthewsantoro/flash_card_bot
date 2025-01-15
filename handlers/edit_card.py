
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db import Database
from handlers.cards import show_card
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
    text = f"<b>📝Карточка #{card.number} </b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}\n\nВыберете, что именно вы хотите изменить"
    keyboard = await create_edit_card_keyboard(card_id=card.id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_"),StateFilter(CardState.view_card))
async def editing_card(callback: CallbackQuery, state: FSMContext):
    card_id = int(callback.data.split(":")[1])
    state.update_data(edit_card_id=card_id)
    if 'front' in callback.data:
        text='Введите передню часть карточки'
        await callback.message.edit_text(text=text)
        await state.set_state(CardState.edit_front)
    else:
        text = 'Введите заднюю часть карточки'
        await state.set_state(CardState.edit_back)
        await callback.message.edit_text(text='Введите передню часть карточки')

@router.message(StateFilter(CardState.edit_front))
async def front_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    cards = data['cards']
    clb = data["msg_callback"]
    card = data['card']
    index = cards.index(card)
    card.question = message.text
    await db.update_card(card)
    await state.update_data(card=card)
    await state.set_state(CardState.view_card)
    await message.delete()
    await show_card(msg=clb.message, index = index, cards=cards,state=state)

@router.message(StateFilter(CardState.edit_back))
async def back_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    cards = data['cards']
    clb = data["msg_callback"]
    card = data['card']
    index = cards.index(card)
    card.answer = message.text
    await db.update_card(card)
    await state.update_data(card=card)
    await state.set_state(CardState.view_card)
    await message.delete()
    await show_card(msg=clb.message, index = index, cards=cards,state=state)

    



