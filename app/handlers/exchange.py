from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

import app.database.requests.remains as rq
import app.keyboards as kb
from app.database.requests.requests import main_menu_back
from app.state import ExchangeMoney

exchange_router = Router()


@exchange_router.message(F.text == "Обмен", StateFilter(default_state))
async def exchange_start(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    """
    Хэндлер нажатия кнопки «Обмен».
    Переводит пользователя в состояние выбора направления обмена.
    """
    await state.set_state(ExchangeMoney.direction)
    await message.answer(
        "Выберите направление обмена:",
        reply_markup=await kb.exchange_keyboard()
    )


@exchange_router.message(ExchangeMoney.direction)
async def exchange_direction(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    """
    Хэндлер выбора направления (Плас. -> Нал. или Нал. -> Плас).
    """
    direction = message.text.strip()

    if direction not in ["Плас. -> Нал.", "Нал. -> Плас"]:
        await message.answer(
            "Ошибка: выберите направление обмена, используя клавиатуру."
        )
        return

    await state.update_data(direction=direction)
    await state.set_state(ExchangeMoney.amount)
    await message.answer("Введите сумму для обмена:")


@exchange_router.message(ExchangeMoney.amount)
async def exchange_amount(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    """
    Хэндлер ввода суммы. Проверяет остатки и обновляет их.
    """
    data = await state.get_data()
    direction = data["direction"]
    user_id = message.from_user.id

    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer("Ошибка: введите числовое "
                             "значение суммы.")
        return

    if amount <= 0:
        await message.answer("Сумма должна быть больше 0. "
                             "Попробуйте снова.")
        return

    remains = await rq.get_remains_for_user(user_id)
    if not remains:
        await message.answer("У вас нет остатков, "
                             "сначала внесите данные (Приход).")
        await state.clear()
        return

    if direction == "Плас. -> Нал.":
        if remains.plastic < amount:
            await message.answer("Недостаточно средств на "
                                 "пластике для обмена.")
            return
        remains.plastic -= amount
        remains.cash += amount
    else:
        if remains.cash < amount:
            await message.answer("Недостаточно наличных "
                                 "для обмена.")
            return
        remains.cash -= amount
        remains.plastic += amount

    await rq.update_remains(remains)

    await state.clear()
    await message.answer(
        f"Обмен успешно выполнен! Текущие остатки:\n"
        f"Наличные: {remains.cash:,.0f} UZS\n"
        f"Пластик: {remains.plastic:,.0f} UZS",
        reply_markup=await kb.expense_arrival_keyboard()
    )
