from aiogram.fsm.state import State, StatesGroup

class CardState(StatesGroup):
    choose_set = State()
    add_set = State()
    enter_question = State()
    enter_answer = State()
    finish = State()
    view_card = State()
    menu_card = State()
    edit_front = State()
    edit_back = State()
    edit_set = State()
    edit_name_set = State()
    
    