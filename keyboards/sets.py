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
    builder.adjust(1) 
    return builder.as_markup()

async def create_set_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Карточки', callback_data='view_cards'))
    builder.add(InlineKeyboardButton(text='Редактировать', callback_data='edit_set'))
    builder.add(InlineKeyboardButton(text='Удалить', callback_data='delete_set'))

async def create_card_keyboard(index: int, total: int):
    builder = InlineKeyboardBuilder()
    if index > 1:
        builder.button(text="⬅️", callback_data=f"carousel:{index-1}")
    if index < total - 1:
        builder.button(text="➡️", callback_data=f"carousel:{index+1}")
    builder.button(text="✏️ Редактировать", callback_data=f"cardedit_{index}")
    builder.button(text="🗑️ Удалить", callback_data=f"carddelete_{index}")
    return builder.as_markup()

async def create_set_setting():
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Редактировать название", callback_data=f"collection_edit")
    builder.add(InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"collection_delete"))
    builder.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"collection_back"))
    return builder.as_markup()