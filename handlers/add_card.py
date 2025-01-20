from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers.cards import show_card
from states.cards import CardState
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.cards import finish_card


router = Router()

db = Database()


@router.message(StateFilter(CardState.enter_question))
async def entering_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(q=message.text)
    data = await state.get_data()
    callback = data["msg_callback"]
    await message.delete()

    await bot.edit_message_text(
        text=f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT:\n </b>{message.text}\n\nНапишите BACK карточки",
        chat_id=message.chat.id,
        message_id=callback.message.message_id,
    )
    await state.set_state(CardState.enter_answer)


@router.message(StateFilter(CardState.enter_answer))
async def entering_answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(a=message.text)
    data = await state.get_data()
    callback = data["msg_callback"]
    card = await db.add_card(
        answer=data["a"],
        question=data["q"],
        deck_id=data["deck"].id,
        number=data["number"],
    )
    cards = data.get("cards")
    if cards is None:
        cards = []
    cards.append(card)

    await state.update_data(cards=cards)
    keyboard = await finish_card()
    await bot.edit_message_text(
        f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT:\n </b>{card.question}\n<b>👇BACK \n</b>:{card.answer}",
        chat_id=message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard,
    )
    await message.delete()
    await state.set_state(CardState.finish)


@router.callback_query(F.data.startswith("card_"), StateFilter(CardState.finish))
async def finish(callback: CallbackQuery, state: FSMContext):
    option = callback.data.split("_")[1]
    data = await state.get_data()
    if option == "new":
        number = data["number"] + 1
        await state.update_data(number=number)
        await state.set_state(CardState.enter_question)
        await callback.message.edit_text(
            text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
            reply_markup=None,
        )
    if option == "finish":
        await state.set_state(CardState.view_card)
        cards = data["cards"]
        await show_card(
            msg=callback.message, index=len(cards) - 1, cards=cards, state=state
        )
