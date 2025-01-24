from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_start_study_keyboard(empty: bool):
    builder = InlineKeyboardBuilder()
    if not empty:
        builder.add(InlineKeyboardButton(text="🧠Учить", callback_data=f"learn_start"))
    builder.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"learn_back"))

    return builder.as_markup()

async def create_study_result_keyboard(card_id : int): 
    builder = InlineKeyboardBuilder()
    builder.row(
    InlineKeyboardButton(text="😵‍💫Забыл", callback_data=f"learn_level:{card_id}:0"),
    InlineKeyboardButton(text="😎Помню", callback_data=f"learn_level:{card_id}:1"))
    builder.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"learn_back"))

    return builder.as_markup()