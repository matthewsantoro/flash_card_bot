from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from handlers.cards import show_card
from states.cards import CardState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.decks import create_deck_setting, create_deck_setting, create_decks_keyboard
from aiogram.fsm.context import FSMContext

router = Router()

db = Database()


@router.message(StateFilter(CardState.add_deck))
async def adding_collection(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    deck = await db.add_deck(name=message.text, creator_id=user_id)
    await state.update_data(deck_id=deck.id)
    await state.set_state(CardState.view_card)
    clb = data["msg_callback"]
    await message.delete()
    await show_card(msg=clb.message, index=None, cards=None, state=state)


@router.callback_query(F.data == "collection_setting")
async def choose_collection_setting(callback: CallbackQuery, state: FSMContext):
    text = f"Выберите действие которое хотетите сделать"
    keyboard = await create_deck_setting()
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data == "collection_edit")
async def editing_name_collection(callback: CallbackQuery, state: FSMContext):
    text = f"Напиши новое название коллекции"
    await callback.message.edit_text(text=text)
    await state.set_state(CardState.edit_name_deck)


@router.message(StateFilter(CardState.edit_name_deck))
async def edited_name_collection(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await db.edit_deck_name(deck_id=data["deck_id"], name=message.text)
    callback = data['msg_callback'] 
    await state.set_state(CardState.view_card)
    await choose_collection_setting(callback=callback, state=state)
    await callback.answer(text="Карточка изменена", show_alert=True)

@router.callback_query(F.data == "collection_delete")
async def deleting_name_collection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deck_id = data['deck_id']
    await db.delete_deck_by_id(deck_id=deck_id)
    await callback.answer(text="Карточка удалена", show_alert=True)
    await choose_collection_setting(callback=callback, state=state)

@router.callback_query(F.data == "collection_back")
async def choose_collection_setting(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cards = data['cards']
    await show_card(msg=callback.message, index=0, cards=cards, state=state)



    