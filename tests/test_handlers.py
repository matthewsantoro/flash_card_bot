import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from collections import deque

# Предположим, что у нас есть такие классы и методы
class CardState(StatesGroup):
    view_card = State()
    training = State()

class Card:
    def __init__(self, number, question, answer, id, level_id=1):
        self.number = number
        self.question = question
        self.answer = answer
        self.id = id
        self.level_id = level_id

class Deck:
    def __init__(self, id):
        self.id = id

class Database:
    async def get_study_cards_by_deck_id(self, deck_id):
        return [Card(number=1, question="Q1", answer="A1", id=1),
                Card(number=2, question="Q2", answer="A2", id=2)]

    async def update_level_card(self, action_successful, card_id):
        pass

    async def get_next_time_to_learn(self):
        return datetime.now()

# Тестовые функции
@pytest.mark.asyncio
async def test_learning_collections():
    # Мокаем необходимые зависимости
    callback = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    state.get_data.return_value = {'deck': Deck(id=1)}
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    with patch('handlers.learn.create_start_study_keyboard', new_callable=AsyncMock) as mock_create_start_study_keyboard:
        mock_create_start_study_keyboard.side_effect = lambda empty: AsyncMock(return_value=MagicMock())

        from handlers.learn import learnig_collections  # Импортируем после патчей

        await learnig_collections(callback, state)

        # Проверяем вызовы функций и состояние
        state.set_state.assert_called_with(CardState.training)
        state.update_data.assert_called()
        callback.message.edit_text.assert_called()

@pytest.mark.asyncio
async def test_go_back_card_view():
    callback = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    state.get_data.return_value = {'cards': [Card(number=1, question="Q1", answer="A1", id=1)],
                                   'card': Card(number=1, question="Q1", answer="A1", id=1)}
    state.set_state = AsyncMock()

    with patch('handlers.cards.show_card', new_callable=AsyncMock) as mock_show_card:
        from handlers.learn import go_back_card_view  # Импортируем после патчей

        await go_back_card_view(callback, state)

        # Проверяем вызовы функций и состояние
        state.set_state.assert_called_with(CardState.view_card)
        mock_show_card.assert_called()

@pytest.mark.asyncio
async def test_starting_learn():
    message = AsyncMock(spec=Message)
    state = AsyncMock(spec=FSMContext)
    state.get_data.return_value = {'study_cards': deque([Card(number=1, question="Q1", answer="A1", id=1)])}

    with patch('handlers.learn.show_study_card', new_callable=AsyncMock) as mock_show_study_card:
        from handlers.learn import startig_learn  # Импортируем после патчей

        await startig_learn(AsyncMock(spec=CallbackQuery), state)

        # Проверяем вызовы функций
        mock_show_study_card.assert_called()

@pytest.mark.asyncio
async def test_checking_result():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = 'learn_level:1:0'
    state = AsyncMock(spec=FSMContext)
    state.get_data.return_value = {'study_cards': deque([Card(number=1, question="Q1", answer="A1", id=1)])}
    state.set_state = AsyncMock()

    with patch('handlers.learn.show_study_card', new_callable=AsyncMock) as mock_show_study_card, \
         patch('handlers.learn.insert_random', new_callable=AsyncMock) as mock_insert_random, \
         patch('database.db.Database.update_level_card', new_callable=AsyncMock) as mock_update_level_card:
        
        from handlers.learn import checking_result  # Импортируем после патчей

        await checking_result(callback, state)

        # Проверяем вызовы функций и состояние
        mock_show_study_card.assert_called()
        mock_update_level_card.assert_called()