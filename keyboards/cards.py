from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def finish_card() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f"Добавить еще карточку",
        callback_data="card_new"))
    builder.add(InlineKeyboardButton(
        text=f"Завершить добавление",
        callback_data="card_finish"))
    builder.adjust(2) 
    return builder.as_markup()