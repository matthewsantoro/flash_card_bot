from collections import deque
import random
from tracemalloc import BaseFilter
from typing import Any, Deque, Optional, Sequence
from aiogram import F, Router
from aiogram.types import  CallbackQuery, Message
from database.db import Database
from handlers.cards import show_card
from keyboards.learn import create_start_study_keyboard, create_study_result_keyboard
from models.models import Card, Deck
from states.cards import CardState
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

router = Router()

db = Database()


@router.callback_query(F.data == "collection_learn", StateFilter(CardState.view_card))
async def learnig_collections(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CardState.training)
    data = await state.get_data()
    deck: Deck = data['deck']
    study_cards: list = await db.get_study_cards_by_deck_id(deck_id=deck.id)
    random.shuffle(study_cards)
    study_cards = deque(study_cards)
    await state.update_data(study_cards=study_cards)
    if study_cards:
        keyboard = await create_start_study_keyboard(empty=False)
        await callback.message.edit_text(f'Карточек на изучение: {len(study_cards)}', reply_markup=keyboard)
    else:
        keyboard = await create_start_study_keyboard(empty=True)
        text = f'У вас нет карточек для узучения'
        time : datetime= await db.get_next_time_to_learn()
        if time: text+=f'\n следущее изучение будет {time.strftime("%d-%m-%Y %H:%M:%S")}'
        await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data == 'learn_back', StateFilter(CardState.training))
async def go_back_card_view(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CardState.view_card)
    data = await state.get_data()
    cards = data['cards']    
    card = data['card']
    index = cards.index(card)
    await show_card(callback.message, index=index, cards=cards, state=state)

@router.callback_query(F.data == 'learn_start', StateFilter(CardState.training))
async def startig_learn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    study_cards = data['study_cards']    
    await show_study_card(callback.message, study_card=study_cards[0], state=state)
    

async def show_study_card(msg: Message, study_card: Optional[Card], state: FSMContext):
        text = f"""<b>📝Карточка #{study_card.number}</b>\n
                    <b>👆FRONT:</b>\n
                    {study_card.question}\n
                    <b>👇BACK</b>:\n
                    <span class="tg-spoiler">{study_card.answer}</span>"""
        keyboard = await create_study_result_keyboard(card_id=study_card.id)
        await msg.edit_text(text=text, reply_markup=keyboard)



@router.callback_query(F.data.startswith('learn_level'), StateFilter(CardState.training))
async def checking_result(callback: CallbackQuery, state: FSMContext):
    card_id = int(callback.data.split(":")[1])
    is_sucseed = bool(int(callback.data.split(":")[2]))
    data = await state.get_data()
    study_cards= data['study_cards']
    study_card: Card = study_cards.popleft()
    if study_card.level_id == 1 and not is_sucseed:
        await insert_random(sequence=study_cards, element=study_card)
    else: 
         await db.update_level_card(action_successful=is_sucseed, card_id=card_id)
    
    await state.update_data(study_cards=study_cards)
    if study_cards:        
        await show_study_card(callback.message, study_card=study_cards[0], state=state)
    else: 
        cards = data['cards']    
        card = data['card']
        index = cards.index(card)
        await state.set_state(CardState.view_card)
        await show_card(callback.message, index=index, cards=cards, state=state)
        await callback.answer(text="Отлично, насегодня вы все изучили", show_alert=True)


async def insert_random(sequence: Sequence[Any] , element):
    if len(sequence) > 1:
        position = random.randint(1, len(sequence))
        sequence.insert(position, element)
    else:
        sequence.append(element)    






