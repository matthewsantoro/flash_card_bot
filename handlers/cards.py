from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from keyboards.menu import create_main_menu
from models.models import Card
from states.cards import CardState
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.cards import create_card_keyboard, create_empty_card_keyboard
from aiogram.fsm.context import FSMContext

from utils.text import EMPTY_CARD_IN_DECK, ENTER_DECK_NAME, MAIN_MENU_TEXT

router = Router()

db = Database()


@router.callback_query(F.data.startswith("deck_"), StateFilter(CardState.choose_deck))
async def checking_chosen_deck(callback: CallbackQuery, state: FSMContext):
    deck_id = int(callback.data.split("_")[1])
    if deck_id == 0:
        await callback.message.edit_text(
            text=ENTER_DECK_NAME, reply_markup=None
        )
        await state.set_state(CardState.add_deck)
        await state.update_data(number=1)
    else:
        await state.update_data(deck_id=deck_id)
        cards = await db.get_cards_by_deck_id(deck_id)
        await state.update_data(cards=cards)
        await show_card(callback.message, 0, cards, state=state)
        await state.set_state(CardState.view_card)


async def show_card(msg: Message, index: Optional[int], cards: Optional[list[Card]], state: FSMContext):
    if cards:
        card = cards[index]
        await state.update_data(card=card)
        keyboard = await create_card_keyboard(index=index, total=len(cards))
        await msg.edit_text(
            text=f"<b>📝Карточка #{card.number}</b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}",
            reply_markup=keyboard,
        )
    else:
        keyboard = await create_empty_card_keyboard()
        await msg.edit_text(
            text=EMPTY_CARD_IN_DECK,
            reply_markup=keyboard,
        )
    


@router.callback_query(F.data.startswith("card_carousel:"))
async def choosing_deck(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    data = await state.get_data()
    cards = data["cards"]
    await show_card(callback.message, index, cards=cards,state=state)


@router.callback_query(F.data == "card_back", StateFilter(CardState.view_card))
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = await create_main_menu()
    await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.callback_query(F.data == "card_add", StateFilter(CardState.view_card))
async def add_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    number = await db.get_last_card_number_in_deck(deck_id=data["deck_id"]) + 1
    await state.update_data(number=number)
    await callback.message.edit_text(
        text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
        reply_markup=None,
    )
    await state.set_state(CardState.enter_question)


@router.callback_query(
    F.data.startswith("card_delete:"), StateFilter(CardState.view_card)
)
async def delete_card(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    data = await state.get_data()
    card = data["cards"].pop(index)
    cards = data["cards"]
    await db.delete_card(card_id=card.id)
    await state.update_data(cards=cards)
    if len(cards) == 0:
        await show_card(msg=callback.message, index=None, cards=None,state=state),
    elif index == len(cards):
        await show_card(msg=callback.message, index=index - 1, cards=cards,state=state)
    else:
        await show_card(msg=callback.message, index=index, cards=cards,state=state)
    await callback.answer(text="Карточка удалена", show_alert=True)
