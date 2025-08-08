from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    birthdate = State()
    country = State()
    location = State()
    phone = State()
    experience = State()
