from aiogram.dispatcher import State, StatesGroup

class AddCard(StatesGroup):
    choose_set = State()
    enter_question = State()
    enter_answer = State()
    finish = State()