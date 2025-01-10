from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from keyboards.menu import create_main_menu
from states.cards import CardState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard
from keyboards.cards import finish_card
from utils.text import MAIN_MENU_TEXT

router = Router()

db = Database()


# @router.callback_query(F.data.startswith("set_"), StateFilter(CardState.choose_set))
# async def choosing_set(callback: CallbackQuery, state: FSMContext):
#     set_id = int(callback.data.split("_")[1])
#     if set_id == 0:
#         await callback.message.edit_text(
#             text="Введите название колекции:", reply_markup=None
#         )
#         await state.set_state(CardState.add_set)
#         await state.update_data(number=1)
#     else:
#         number = await db.get_last_card_number_in_set(set_id=set_id) + 1
#         await state.update_data(card_message_id=callback.message.message_id)
#         await state.update_data(number=number)
#         await state.update_data(set_id=set_id)
#         # await callback.message.edit_text(
#         #     text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
#         #     reply_markup=None,
#         # )
#         # #await state.set_state(CardState.enter_question)
#         await state.set_state(CardState.view_card)


@router.message(StateFilter(CardState.add_set))
async def add_set(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    new_set = await db.add_set(creator_id=user_id, name=message.text)
    data = await state.get_data()

    await state.update_data(set_id=new_set.id)
    await state.set_state(CardState.enter_question)

    await bot.edit_message_text(
        text=f"Коллекция '{new_set.name}' добавлена.\n<b>📝Карточка #{data['number']}</b>\n Напишите Front карточки",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
    )
    await message.delete()

async def add_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(q=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(
        text=f"<b>📝Карточка #{data['number']}</b>\n<b>👆FRONT: </b>{message.text}\n\nНапишите BACK карточки",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
    )

@router.message(StateFilter(CardState.enter_question))
async def entering_question(message: Message, state: FSMContext, bot: Bot):
    await add_question(message = message, state=state, bot=bot)
    await state.set_state(CardState.enter_answer)




@router.message(StateFilter(CardState.enter_answer))
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
    await state.set_state(CardState.finish)


@router.callback_query(F.data.startswith("card_"), StateFilter(CardState.finish))
async def finish(callback: CallbackQuery, state: FSMContext):
    option = callback.data.split("_")[1]
    data = await state.get_data()
    number = data["number"] + 1
    await state.update_data(number=number)
    if option == "new":
        await state.set_state(CardState.enter_question)
        await callback.message.edit_text(
            text=f"<b>📝Карточка #{number}</b>\nНапишите Front карточки",
            reply_markup=None,
        )
    if option == "finish":
        await state.clear()
        keyboard = await create_main_menu()
        await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)



