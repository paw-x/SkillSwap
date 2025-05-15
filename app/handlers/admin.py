# app/handlers/admin.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import re
from app.database import db
from app.locales import translations

router = Router()

# Проверка прав администратора
def is_admin(user_id: int) -> bool:
    return user_id in [db.ADMIN_ID_FIRST, db.ADMIN_ID_SECOND]

@router.message(Command("addpeople"))
async def add_user_admin(message: Message):
    # Проверка прав
    if not is_admin(message.from_user.id):
        await message.answer("❌ Эта команда доступна только администраторам!")
        return

    # Парсинг команды с помощью регулярного выражения
    pattern = r"""
        ^/addpeople\s+
        (\d+)\s+                       # tg_id
        ([^(]+?)\s+                    # name
        \((.+?)\)\s+                   # bio
        (начинающий|средний|профи)\s+  # experience_level
        (ru|en|zh)\s+                  # language
        \((.+?)\)\s+                   # learn_skills
        \((.+?)\)$                     # teach_skills
    """
    match = re.search(pattern, message.text, re.VERBOSE | re.IGNORECASE)

    if not match:
        await message.answer("❌ Неверный формат команды. Пример:\n"
                            "/addpeople 12345678 Имя (Био) средний ru (навыки для изучения) (навыки для преподавания)")
        return

    # Извлечение данных
    tg_id = int(match.group(1))
    name = match.group(2).strip()
    bio = match.group(3).strip()
    experience = match.group(4).lower()
    language = match.group(5).lower()
    learn_skills = [s.strip() for s in match.group(6).split(",")]
    teach_skills = [s.strip() for s in match.group(7).split(",")]

    # Добавление пользователя
    user_id = db.DBManager.add_user(tg_id, name, bio, language, experience)
    if not user_id:
        await message.answer("❌ Пользователь уже существует!")
        return

    # Добавление навыков
    for skill in learn_skills:
        db.DBManager.link_user_skill(tg_id, skill, "learn")
    for skill in teach_skills:
        db.DBManager.link_user_skill(tg_id, skill, "teach")

    await message.answer(f"✅ Пользователь {name} успешно добавлен!")