from typing import Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def finish_card() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=f"Добавить еще карточку", callback_data="card_new")
    )
    builder.add(
        InlineKeyboardButton(text=f"Завершить добавление", callback_data="card_finish")
    )
    builder.adjust(2)
    return builder.as_markup()


async def create_card_keyboard(index: int, total: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if index > 0:
        builder.add(
            InlineKeyboardButton(
                text="⬅️ Назад", callback_data=f"card_carousel:{index - 1}"
            )
        )
    if index < total - 1:
        builder.add(
            InlineKeyboardButton(
                text="➡️ Вперед", callback_data=f"card_carousel:{index + 1}"
            )
        )
    builder.row(
        InlineKeyboardButton(text="✍️", callback_data=f"card_edit:{index}"),
        InlineKeyboardButton(text="➕", callback_data=f"card_add"),
        InlineKeyboardButton(text="🗑️", callback_data=f"card_delete:{index}"),
        InlineKeyboardButton(text="🔙", callback_data=f"card_back"),
    )
    return builder.as_markup()


async def create_empty_card_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕", callback_data=f"card_add"),
        InlineKeyboardButton(text="🔙", callback_data=f"card_back"),
    )
    return builder.as_markup()

async def create_edit_card_keyboard(card_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="FRONT", callback_data=f"edit_front:{card_id}"),
        InlineKeyboardButton(text="BACK", callback_data=f"edit_back:{card_id}"),
    )
    return builder.as_markup()