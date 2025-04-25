from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="ru"),
            InlineKeyboardButton(text="English", callback_data="en"),
            InlineKeyboardButton(text="中文", callback_data="zh")
        ]
    ])