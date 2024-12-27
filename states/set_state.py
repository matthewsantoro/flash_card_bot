from aiogram.fsm.state import State, StatesGroup

class SetState(StatesGroup):
    choose_set = State()
    menu_set = State()
    menu_card = State()