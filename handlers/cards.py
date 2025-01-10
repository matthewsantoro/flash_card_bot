from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers.add_card import add_question
from keyboards.menu import create_main_menu
from models.models import Card
from states.add_card_state import AddCard
from states.cards import CardState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.cards import create_card_keyboard, finish_card
from aiogram.fsm.context import FSMContext

from utils.text import MAIN_MENU_TEXT

router = Router()

db = Database()


@router.callback_query(F.data.startswith("set_"), StateFilter(AddCard.choose_set))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    set_id = int(callback.data.split("_")[1])
    if set_id == 0:
        await callback.message.edit_text(
            text="Введите название колекции:", reply_markup=None
        )
        await state.set_state(AddCard.add_set)
        await state.update_data(number=1)
    else:
        number = await db.get_last_card_number_in_set(set_id=set_id) + 1
        await state.update_data(card_message_id=callback.message.message_id)
        await state.update_data(number=number)
        await state.update_data(set_id=set_id)
        await callback.message.edit_text(
            text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
            reply_markup=None,
        )
        await state.set_state(AddCard.enter_question)


@router.message(StateFilter(AddCard.add_set))
async def add_set(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    new_set = await db.add_set(creator_id=user_id, name=message.text)
    data = await state.get_data()

    await state.update_data(set_id=new_set.id)
    await state.set_state(AddCard.enter_question)

    await bot.edit_message_text(
        text=f"Коллекция '{new_set.name}' добавлена.\n<b>📝Карточка #{data['number']}</b>\n Напишите Front карточки",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
    )
    await message.delete()


@router.message(StateFilter(AddCard.enter_question))
async def entering_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(q=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(
        text=f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT: </b>{message.text}\n\nНапишите BACK карточки",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
    )
    await state.set_state(AddCard.enter_answer)


@router.message(StateFilter(AddCard.enter_answer))
async def entering_answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(a=message.text)
    data = await state.get_data()
    card = await db.add_card(
        answer=data["a"],
        question=data["q"],
        set_id=data["set_id"],
        number=data["number"],
    )
    keyboard = await finish_card()
    await bot.edit_message_text(
        f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=keyboard,
    )
    await message.delete()
    await state.set_state(AddCard.finish)


@router.callback_query(F.data.startswith("card_"), StateFilter(AddCard.finish))
async def finish(callback: CallbackQuery, state: FSMContext):
    option = callback.data.split("_")[1]
    data = await state.get_data()
    number = data["number"] + 1
    await state.update_data(number=number)
    if option == "new":
        await state.set_state(AddCard.enter_question)
        await callback.message.edit_text(
            text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
            reply_markup=None,
        )
    if option == "finish":
        await state.clear()
        keyboard = await create_main_menu()
        await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)



@router.callback_query(F.data.startswith("set_"), StateFilter(CardState.choose_set))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    set_id = int(callback.data.split("_")[1])
    cards = await db.get_cards_by_set_id(set_id)
    await state.update_data(cards=cards)
    await show_card(callback.message, 0, cards)
    await state.set_state(CardState.view_card)


async def show_card(msg: Message, index: int, cards: list[Card]):
    card = cards[index]
    keyboard = await create_card_keyboard(index=index, total=len(cards))
    await msg.edit_text(
        text=f"<b>📝Карточка #{card.number}</b>\n<b>👆FRONT: </b>{card.question}\n<b>👇BACK </b>:{card.answer}",
        reply_markup=keyboard,
    )




@router.callback_query(F.data.startswith("card_carousel:"))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])

    data = await state.get_data()
    cards = data["cards"]
    await show_card(callback.message, index, cards)


@router.callback_query(F.data == 'card_back', StateFilter(CardState.view_card))
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = await create_main_menu()
    await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)

@router.callback_query(F.data == 'card_add', StateFilter(CardState.view_card))
async def add_card(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await add_question(message=callback.message, state=state, bot=bot)
    