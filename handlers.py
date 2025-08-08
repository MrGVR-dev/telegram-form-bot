import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states import Form
from localizations import RU, UZ

load_dotenv()
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK")
HTTP_TIMEOUT = 10

router = Router()

# Валидаторы
NAME_CITY_RE = re.compile(r"^[A-Za-zА-Яа-яЁёЎўҚқҲҳҒғ\s\-]{2,50}$")
PHONE_RE = re.compile(r"^\+?\d{7,20}$")

def is_valid_text(text: str) -> bool:
    return bool(NAME_CITY_RE.fullmatch(text.strip()))

def is_valid_phone(text: str) -> bool:
    return bool(PHONE_RE.fullmatch(text.strip()))

def is_valid_date(text: str) -> bool:
    try:
        dt = datetime.strptime(text.strip(), "%d.%m.%Y")
        return 1900 <= dt.year <= 2100
    except ValueError:
        return False

def is_valid_experience(text: str) -> bool:
    return text.isdigit() and 0 <= int(text) <= 60

async def get_locales(state: FSMContext):
    data = await state.get_data()
    return RU if data.get("lang", "ru") == "ru" else UZ

# /start — выбор языка
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbek")]],
        resize_keyboard=True
    )
    await message.answer("Выберите язык / Tilni tanlang:", reply_markup=kb)

# Выбор языка
@router.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def set_language(message: Message, state: FSMContext):
    lang = "ru" if message.text.startswith("🇷🇺") else "uz"
    await state.set_data({"lang": lang})
    loc = await get_locales(state)
    await state.set_state(Form.name)
    await message.answer(loc["enter_name"], reply_markup=ReplyKeyboardRemove())

# Имя
@router.message(Form.name)
async def handle_name(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_text(message.text):
        return await message.answer(loc["only_text"].format(example="Али"))
    await state.update_data(name=message.text.strip())
    await state.set_state(Form.birthdate)
    await message.answer(loc["enter_birthdate"])

# Дата рождения
@router.message(Form.birthdate)
async def handle_birthdate(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_date(message.text):
        return await message.answer(loc["invalid_date"].format(example="10.05.2002"))
    await state.update_data(birthdate=message.text.strip())
    await state.set_state(Form.country)
    await message.answer(loc["enter_country"])

# Страна
@router.message(Form.country)
async def handle_country(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_text(message.text):
        return await message.answer(loc["only_text"].format(example="Узбекистан"))
    await state.update_data(country=message.text.strip())
    await state.set_state(Form.location)
    await message.answer(loc["enter_city"])

# Город
@router.message(Form.location)
async def handle_location(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_text(message.text):
        return await message.answer(loc["only_text"].format(example="Ташкент"))
    await state.update_data(location=message.text.strip())
    await state.set_state(Form.phone)
    await message.answer(loc["enter_phone"])

# Телефон
@router.message(Form.phone)
async def handle_phone(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_phone(message.text):
        return await message.answer(loc["only_numbers"].format(example="998901234567"))
    await state.update_data(phone=message.text.strip())
    await state.set_state(Form.experience)
    await message.answer(loc["enter_experience"])

# Опыт
@router.message(Form.experience)
async def handle_experience(message: Message, state: FSMContext):
    loc = await get_locales(state)
    if not is_valid_experience(message.text):
        return await message.answer(loc["only_numbers"].format(example="3"))

    await state.update_data(experience=message.text.strip())
    payload = await state.get_data()

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        await message.answer(f"⚠️ Не удалось отправить данные ({e}). Попробуйте позже.")
        return

    await message.answer(loc["form_complete"], reply_markup=ReplyKeyboardRemove())
    await state.clear()
