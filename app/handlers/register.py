from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.register import RegisterState
from database import db

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(RegisterState.name)
    await message.answer("Привет! Давай зарегистрируемся.\nКак тебя зовут?")

@router.message(RegisterState.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterState.bio)
    await message.answer("Расскажи немного о себе (bio):")

@router.message(RegisterState.bio)
async def register_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await state.set_state(RegisterState.language)
    await message.answer("На каком языке ты хочешь общаться?")

@router.message(RegisterState.language)
async def register_language(message: Message, state: FSMContext):
    await state.update_data(language=message.text)
    await state.set_state(RegisterState.experience)
    await message.answer("Какой у тебя уровень опыта? (начинающий / средний / профи)")

@router.message(RegisterState.experience)
async def register_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(RegisterState.skills_to_teach)
    await message.answer("Какие навыки ты можешь преподавать? (через запятую)")

@router.message(RegisterState.skills_to_teach)
async def register_teach(message: Message, state: FSMContext):
    await state.update_data(skills_to_teach=message.text)
    await state.set_state(RegisterState.skills_to_learn)
    await message.answer("Какие навыки ты хочешь изучить? (через запятую)")

@router.message(RegisterState.skills_to_learn)
async def register_learn(message: Message, state: FSMContext):
    data = await state.get_data()
    db.add_user(
        tg_id=message.from_user.id,
        name=data["name"],
        bio=data["bio"],
        language=data["language"],
        experience=data["experience"]
    )

    for skill in data["skills_to_teach"].split(","):
        db.link_user_skill(message.from_user.id, skill.strip(), "teach")
    for skill in message.text.split(","):
        db.link_user_skill(message.from_user.id, skill.strip(), "learn")

    await message.answer("Спасибо! Ты зарегистрирован.")
    await state.clear()
