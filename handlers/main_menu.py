from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.db import Database
from keyboards.decks import create_decks_keyboard
from states.cards import CardState
from utils.text import MAIN_MENU_TEXT
from keyboards.menu import create_main_menu

router = Router()
db = Database()


@router.message(Command("menu"))  # [2]
async def main_menu(message: Message, state: FSMContext):
    keyboard = await create_main_menu()
    await message.answer(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.callback_query(F.data == "menu_cards")
async def cmd_add_card(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    decks = await db.get_decks_by_user_id(user_id)
    await state.update_data(msg_callback=callback)
    keyboard = await create_decks_keyboard(decks=decks)
    await callback.message.edit_text(
        text="Выберите коллекцию в которую вы хотите добавить карточку:",
        reply_markup=keyboard,
    )
    await state.set_state(CardState.choose_deck)


