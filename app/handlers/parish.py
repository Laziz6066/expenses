from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

import app.database.requests.parishes as rq
import app.keyboards as kb
from app.database.requests.requests import main_menu_back
from app.state import AddParishes

parish_router = Router()


@parish_router.message(F.text == "Приход")
async def parishes_handler(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    await state.set_state(AddParishes.title)
    await message.answer("Введите название:")


@parish_router.message(AddParishes.title)
async def add_title_parishes(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    title = message.text.strip()
    if title == "На главную":
        await state.clear()
        await message.answer(
            "Выберите нужную кнопку:",
            reply_markup=await kb.expense_arrival_keyboard()
        )
        return
    if title in ["Пластик картой", "Расход", "Наличными", "Отчёт"]:
        await message.answer(
            "Ошибка: Похоже, вы случайно нажали на кнопку! "
            "Введите правильное название расхода."
        )
        return
    await state.update_data(title=title)
    await state.set_state(AddParishes.amount)
    await message.answer("Введите сумму:")


@parish_router.message(AddParishes.amount)
async def add_amount_parishes(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer("Ошибка: введено не числовое значение. "
                             "Пожалуйста, введите корректную сумму.")
        return
    if amount < 0:
        await message.answer(
            "Ошибка: Сумма должна быть больше 0."
        )
        return
    await state.update_data(amount=amount)
    await state.set_state(AddParishes.type_parishes)
    await message.answer("Выберите тип прихода:",
                         reply_markup=await kb.type_money())


@parish_router.message(AddParishes.type_parishes)
async def add_type_expense_parishes(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    choice = message.text.strip()
    # Проверяем, что выбор соответствует допустимым вариантам
    if choice not in ["Наличными", "Пластик картой"]:
        await message.answer(
            "Ошибка: выберите корректный тип прихода, используя клавиатуру. "
            "Доступные варианты: Наличными или Пластик картой.",
            reply_markup=await kb.type_money()
        )
        return
    await state.update_data(type_parishes=message.text.strip())
    data = await state.get_data()
    await rq.add_parishes(
        title=data['title'],
        amount=data['amount'],
        type_parishes=data['type_parishes'],
        user_id=message.from_user.id
    )
    await state.clear()

    await message.answer("Данные записаны",
                         reply_markup=await kb.expense_arrival_keyboard())
