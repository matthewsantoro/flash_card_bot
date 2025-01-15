from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from handlers.cards import show_card
from states.cards import CardState
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard
from aiogram.fsm.context import FSMContext
router = Router()

db = Database()

@router.message(StateFilter(CardState.add_set))
async def adding_collection(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id 
    data = await state.get_data()
    collection = await db.add_set(name=message.text, creator_id=user_id)
    await state.update_data(set_id=collection.id)
    await state.set_state(CardState.view_card)
    clb = data["msg_callback"]
    await message.delete()
    await show_card(msg=clb.message, index=None, cards=None,state=state)
    
    