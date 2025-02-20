from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

import app.database.requests.expense as rq
import app.keyboards as kb
from app.database.requests.requests import main_menu_back
from app.state import AddExpenditure

expense_router = Router()


@expense_router.message(F.text == "Расход", StateFilter(default_state))
async def expense_handler(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    await state.set_state(AddExpenditure.title)
    await message.answer("Введите название:")


@expense_router.message(AddExpenditure.title)
async def add_title_expense(message: Message, state: FSMContext):
    # Проверяем, не нажал ли пользователь "На главную"
    if await main_menu_back(message.text.strip(), state, message):
        return  # Если нажал, выходим из хендлера

    title = message.text.strip()

    if title in ["Приход", "Пластик картой", "Наличными", "Отчёт"]:
        await message.answer(
            "Ошибка: Похоже, вы случайно нажали на кнопку! "
            "Введите правильное название расхода."
        )
        return

    await state.update_data(title=title)
    await state.set_state(AddExpenditure.amount)
    await message.answer("Введите сумму:")


@expense_router.message(AddExpenditure.amount)
async def add_amount_expense(message: Message, state: FSMContext):
    # Проверяем, не нажал ли пользователь "На главную"
    if await main_menu_back(message.text.strip(), state, message):
        return  # Если нажал, выходим из хендлера

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
    await state.set_state(AddExpenditure.type_expense)
    await message.answer("Выберите тип расхода:",
                         reply_markup=await kb.type_money())


@expense_router.message(AddExpenditure.type_expense)
async def add_type_expense_expense(message: Message, state: FSMContext):
    # Проверяем, не нажал ли пользователь "На главную"
    if await main_menu_back(message.text.strip(), state, message):
        return  # Если нажал, выходим из хендлера

    choice = message.text.strip()
    # Проверяем, что выбор соответствует допустимым вариантам
    if choice not in ["Наличными", "Пластик картой"]:
        await message.answer(
            "Ошибка: выберите корректный тип расхода, используя клавиатуру. "
            "Доступные варианты: Наличными или Пластик картой.",
            reply_markup=await kb.type_money()
        )
        return

    await state.update_data(type_expense=choice)
    data = await state.get_data()

    # Пытаемся добавить расход и получаем статус
    success, response_message = await rq.add_expenses(
        title=data['title'],
        amount=data['amount'],
        type_expense=data['type_expense'],
        user_id=message.from_user.id
    )

    if not success:
        await message.answer(response_message)
        return

    await state.clear()
    await message.answer("Данные записаны",
                         reply_markup=await kb.expense_arrival_keyboard())
