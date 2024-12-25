from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_sets_keyboard(sets) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for set_item in sets:
        builder.add(InlineKeyboardButton(
            text=f"{set_item.name}",
            callback_data=f"set_{set_item.id}")
        )
    builder.add(InlineKeyboardButton(
        text=f"Добавить набор",
        callback_data="set_0"))
    return builder.as_markup()