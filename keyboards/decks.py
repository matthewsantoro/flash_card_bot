from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_decks_keyboard(decks) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for deck_item in decks:
        builder.add(InlineKeyboardButton(
            text=f"{deck_item.name}",
            callback_data=f"deck_{deck_item.id}")
        )
    builder.add(InlineKeyboardButton(
        text=f"Добавить набор",
        callback_data="deck_0"))
    builder.adjust(1) 
    return builder.as_markup()

async def create_deck_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Карточки', callback_data='view_cards'))
    builder.add(InlineKeyboardButton(text='Редактировать', callback_data='edit_deck'))
    builder.add(InlineKeyboardButton(text='Удалить', callback_data='delete_deck'))

    return builder.as_markup()

async def create_card_keyboard(index: int, total: int):
    builder = InlineKeyboardBuilder()
    if index > 1:
        builder.button(text="⬅️", callback_data=f"carousel:{index-1}")
    if index < total - 1:
        builder.button(text="➡️", callback_data=f"carousel:{index+1}")
    builder.button(text="✏️ Редактировать", callback_data=f"cardedit_{index}")
    builder.button(text="🗑️ Удалить", callback_data=f"carddelete_{index}")
    return builder.as_markup()

async def create_deck_setting():
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Редактировать название", callback_data=f"collection_edit")
    builder.add(InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"collection_delete"))
    builder.add(InlineKeyboardButton(text="🔙Назад", callback_data=f"collection_back"))
    return builder.as_markup()