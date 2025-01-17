from aiogram.fsm.state import State, StatesGroup

class CardState(StatesGroup):
    choose_deck = State()
    add_deck = State()
    enter_question = State()
    enter_answer = State()
    finish = State()
    view_card = State()
    menu_card = State()
    edit_front = State()
    edit_back = State()
    edit_deck = State()
    edit_name_deck = State()
    
    