from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.register import RegisterState
from app.database import db
from app.locales import translations
import app.handlers.keyboards as kb

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(RegisterState.language)
    await message.answer(
        text="Choose your language:",  # Первое сообщение всегда на английском
        reply_markup=kb.get_language_keyboard()
    )


@router.callback_query(RegisterState.language, F.data.in_(["ru", "en", "zh"]))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data
    await state.update_data(language=lang)
    await state.set_state(RegisterState.name)

    # Получаем перевод для следующего сообщения
    text = translations[lang]["ask_name"]
    await callback.message.answer(text)
    await callback.answer()


@router.message(RegisterState.name)
async def register_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")

    await state.update_data(name=message.text)
    await state.set_state(RegisterState.bio)
    await message.answer(translations[lang]["ask_bio"])


@router.message(RegisterState.bio)
async def register_bio(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")

    await state.update_data(bio=message.text)
    await state.set_state(RegisterState.experience)
    await message.answer(translations[lang]["ask_experience"])


@router.message(RegisterState.experience)
async def register_experience(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")

    await state.update_data(experience=message.text)
    await state.set_state(RegisterState.skills_to_teach)
    await message.answer(translations[lang]["ask_teach"])


@router.message(RegisterState.skills_to_teach)
async def register_teach(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")

    await state.update_data(skills_to_teach=message.text)
    await state.set_state(RegisterState.skills_to_learn)
    await message.answer(translations[lang]["ask_learn"])


@router.message(RegisterState.skills_to_learn)
async def register_learn(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")

    # Сохраняем данные в БД
    user_id = db.DBManager.add_user(
        tg_id=message.from_user.id,
        name=data["name"],
        bio=data["bio"],
        language=data["language"],
        experience_level=data["experience"]
    )

    for skill in data["skills_to_teach"].split(","):
        db.DBManager.link_user_skill(
            message.from_user.id,
            skill.strip(),
            "teach"
        )
    for skill in message.text.split(","):
        db.DBManager.link_user_skill(
            message.from_user.id,
            skill.strip(),
            "learn"
        )

    await message.answer(translations[lang]["registration_complete"])
    await state.clear()