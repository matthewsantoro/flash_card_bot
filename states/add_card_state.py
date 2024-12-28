from aiogram.fsm.state import State, StatesGroup

class AddCard(StatesGroup):
    choose_set = State()
    add_set = State()
    enter_question = State()
    enter_answer = State()
    finish = State()
    