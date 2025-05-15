# app/handlers/profile.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.database import db
from app.locales import translations
from .keyboards import get_main_menu

router = Router()


@router.message(F.text == "👤 Профиль")
@router.message(F.text == "/profile")
async def show_profile(message: Message):
    user = db.DBManager.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ Сначала зарегистрируйтесь через /start")
        return

    # Формируем текст профиля
    profile_text = (
        f"👤 *{user['name']}*\n"
        f"📝 *О себе:* {user['bio']}\n"
        f"📈 *Уровень опыта:* {user['experience_level']}\n"
        f"🌐 *Язык:* {user['language']}"
    )

    await message.answer(
        text=profile_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )