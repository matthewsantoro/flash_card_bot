from aiogram.fsm.state import State, StatesGroup

class CardState(StatesGroup):
    choose_set = State()
    view_card = State()
    menu_card = State()