from typing import Optional
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from keyboards.menu import create_main_menu
from models.models import Card
from states.cards import CardState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.cards import create_card_keyboard, create_empty_card_keyboard
from aiogram.fsm.context import FSMContext

from utils.text import EMPTY_CARD_IN_SET, MAIN_MENU_TEXT

router = Router()

db = Database()


@router.callback_query(F.data.startswith("set_"), StateFilter(CardState.choose_set))
async def checking_chosen_set(callback: CallbackQuery, state: FSMContext):
    set_id = int(callback.data.split("_")[1])
    if set_id == 0:
        await callback.message.edit_text(
            text="Введите название колекции:", reply_markup=None
        )
        await state.set_state(CardState.add_set)
        await state.update_data(number=1)
    else:
        await state.update_data(set_id=set_id)
        cards = await db.get_cards_by_set_id(set_id)
        await state.update_data(cards=cards)
        await show_card(callback.message, 0, cards)
        await state.set_state(CardState.view_card)


async def show_card(msg: Message, index: Optional[int], cards: Optional[list[Card]]):
    if cards:
        card = cards[index]
        keyboard = await create_card_keyboard(index=index, total=len(cards))
        await msg.edit_text(
            text=f"<b>📝Карточка #{card.number}</b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}",
            reply_markup=keyboard,
        )
    else:
        keyboard = await create_empty_card_keyboard()
        await msg.edit_text(
            text=EMPTY_CARD_IN_SET,
            reply_markup=keyboard,
        )




@router.callback_query(F.data.startswith("card_carousel:"))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])

    data = await state.get_data()
    cards = data["cards"]
    await show_card(callback.message, index, cards)


@router.callback_query(F.data == "card_back", StateFilter(CardState.view_card))
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = await create_main_menu()
    await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.callback_query(F.data == "card_add", StateFilter(CardState.view_card))
async def add_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    number = await db.get_last_card_number_in_set(set_id=data["set_id"]) + 1
    await state.update_data(number=number)
    await callback.message.edit_text(
        text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
        reply_markup=None,
    )
    await state.set_state(CardState.enter_question)

@router.callback_query(F.data.startswith("card_delete:"),StateFilter(CardState.view_card))
async def delete_card(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    data = await state.get_data()
    card = data["cards"].pop(index)
    cards = data["cards"]
    await db.delete_card(card_id=card.id)
    await state.update_data(cards=cards)
    if len(cards) == 0:
        await show_card(msg=callback.message, index=None, cards=None)
    elif index == len(cards):
        await show_card(msg=callback.message, index=index-1, cards=cards)
    else:
        await show_card(msg=callback.message, index=index, cards=cards)
    await callback.answer(text='Карточка удалена', show_alert=True)
    