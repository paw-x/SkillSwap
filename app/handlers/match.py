# app/handlers/match.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import db
from app.locales import translations

router = Router()


@router.message(F.text == "🔍 Найти ментора")
async def find_mentors(message: Message):
    user = db.DBManager.get_user(message.from_user.id)

    if not user:
        await message.answer(translations[user['language']]["profile_not_found"])
        return

    mentors = db.DBManager.find_mentors(message.from_user.id)

    if not mentors:
        await message.answer("😔 Пока нет подходящих менторов. Попробуйте позже!")
        return

    response = ["🔍 *Найдены менторы:*\n"]
    for idx, mentor in enumerate(mentors, 1):
        response.append(
            f"{idx}. {mentor['name']}\n"
            f"   📝 Опыт: {mentor['experience_level']}\n"
            f"   🌐 Язык: {mentor['language']}\n"
        )

    # Кнопка для обновления списка
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Обновить список", callback_data="refresh_mentors")

    await message.answer(
        "\n".join(response),
        parse_mode="Markdown",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "refresh_mentors")
async def refresh_mentors(callback: CallbackQuery):
    await find_mentors(callback.message)
    await callback.answer()