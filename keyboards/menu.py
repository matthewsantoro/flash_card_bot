from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f"🗂️Наборы карточек",
        callback_data="menu_set"))
    builder.add(InlineKeyboardButton(
        text=f"📝Карточки",
        callback_data="menu_cards"))
    builder.add(InlineKeyboardButton(
        text=f"⚙️Найстроки",
        callback_data="menu_setting"))
    builder.add(InlineKeyboardButton(
        text=f"🤔Проверка знаний",
        callback_data="menu_setting"))
    builder.adjust(2) 
    return builder.as_markup()