from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    language = State()
    name = State()
    bio = State()
    experience = State()
    skills_to_teach = State()
    skills_to_learn = State()