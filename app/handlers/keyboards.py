from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="ru"),
            InlineKeyboardButton(text="English", callback_data="en"),
            InlineKeyboardButton(text="中文", callback_data="zh")
        ]
    ])


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="🔍 Найти ментора"), KeyboardButton(text="📅 Мои сессии")]
        ],
        resize_keyboard=True
    )


def get_profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
        ]
    ])