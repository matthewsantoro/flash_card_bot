from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from handlers import main_menu
from keyboards.menu import create_main_menu
from states.add_card_state import AddCard
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.sets import create_sets_keyboard
from keyboards.cards import finish_card
from utils.text import MAIN_MENU_TEXT

router = Router()



@router.callback_query(F.data.startswith("menu_addcard"))
async def cmd_add_card(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    db = Database()
    sets = await db.get_sets_by_user_id(user_id)
    keyboard = await create_sets_keyboard(sets=sets)
    await callback.message.edit_text(
        text="Выберите набор в который вы хотите добавить карточку:",
        reply_markup=keyboard,
    )
    await state.set_state(AddCard.choose_set)


@router.callback_query(F.data.startswith("set_"), StateFilter(AddCard.choose_set))
async def choosing_set(callback: CallbackQuery, state: FSMContext):
    set_id = int(callback.data.split("_")[1])
    if set_id == 0:
        await callback.message.edit_text(text="Введите название набора:", reply_markup=None)
        await state.set_state(AddCard.add_set)
    else:
        await state.update_data(set_id=set_id)
        await callback.message.edit_text(text="Введите Вопрос:", reply_markup=None)
        await state.set_state(AddCard.enter_question)


@router.message(StateFilter(AddCard.add_set))
async def add_set(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db = Database()
    new_set = await db.add_set(creator_id=user_id, name=message.text)
    await message.reply(f"Набор '{new_set.name}' добавлен.")
    await state.update_data(set_id=new_set.id)
    await state.set_state(AddCard.enter_question)
    await message.edit_text(text="Введите Вопрос:", reply_markup=None)




@router.message(StateFilter(AddCard.enter_question))
async def entering_question(message: Message, state: FSMContext):
    await state.update_data(q=message.text)
    await message.reply(f"Вопрос записан. Введите ответ")
    await state.set_state(AddCard.enter_answer)

@router.message(StateFilter(AddCard.enter_answer))
async def entering_answer(message: Message, state: FSMContext):   
    await state.update_data(a=message.text)
    data = await state.get_data()
    db = Database()
    card = await db.add_card(answer=data["a"], question=data['q'], set_id=data["set_id"])
    keyboard = await finish_card()
    await message.reply(f"Карточка готова!\nВопрос:\n{card.question}\nОтвет:\n{card.answer} ", reply_markup=keyboard)
    await state.set_state(AddCard.finish)


@router.callback_query(F.data.startswith('card_'), StateFilter(AddCard.finish))
async def finish(callback: CallbackQuery, state: FSMContext): 
    option = callback.data.split("_")[1]
    if option == 'new':
        await state.set_state(AddCard.enter_question)
        await callback.message.answer(text="Введите Вопрос:")
    if option == 'finish':
        await state.clear()
        keyboard = await create_main_menu()
        await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)





