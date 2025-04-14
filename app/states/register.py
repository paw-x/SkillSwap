from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    name = State()
    bio = State()
    language = State()
    experience = State()
    skills_to_teach = State()
    skills_to_learn = State()
