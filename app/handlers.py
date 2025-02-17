from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from app.state import AddParishes, AddExpenditure, AddRemains
import app.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Выберите нужную кнопку:", reply_markup=await kb.expense_arrival_keyboard())


@router.message(F.text == "Отчёт")
async def report_handler(message: Message):
    await message.answer('Выберите нужный вам отчёт!', reply_markup=await kb.expenses_report_keyboard())


@router.message(F.text == "Расход")
async def expense_handler(message: Message, state: FSMContext):
    await state.set_state(AddExpenditure.title)
    await message.answer("Введите название:")


@router.message(AddExpenditure.title)
async def add_title_expense(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddExpenditure.amount)
    await message.answer("Введите сумму:")


@router.message(AddExpenditure.amount)
async def add_amount_expense(message: Message, state: FSMContext):
    await state.update_data(amount=int(message.text.strip()))
    await state.set_state(AddExpenditure.type_expense)
    await message.answer("Выберите тип расхода:", reply_markup=await kb.type_money())


@router.message(AddExpenditure.type_expense)
async def add_type_expense_expense(message: Message, state: FSMContext):
    await state.update_data(type_expense=message.text.strip())
    data = await state.get_data()
    await rq.add_expenses(
        title=data['title'],
        amount=data['amount'],
        type_expense=data['type_expense']
    )
    await state.clear()

    await message.answer("Данные записаны", reply_markup=await kb.expense_arrival_keyboard())


@router.message(F.text == "Приход")
async def parishes_handler(message: Message, state: FSMContext):
    await state.set_state(AddParishes.title)
    await message.answer("Введите название:", reply_markup=await kb.type_money())


@router.message(AddParishes.title)
async def add_title_parishes(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddParishes.amount)
    await message.answer("Введите сумму:")


@router.message(AddParishes.amount)
async def add_amount_parishes(message: Message, state: FSMContext):
    await state.update_data(amount=int(message.text.strip()))
    await state.set_state(AddParishes.type_parishes)
    await message.answer("Выберите тип прихода:", reply_markup=await kb.type_money())


@router.message(AddParishes.type_parishes)
async def add_type_expense_parishes(message: Message, state: FSMContext):
    await state.update_data(type_parishes=message.text.strip())
    data = await state.get_data()
    await rq.add_parishes(
        title=data['title'],
        amount=data['amount'],
        type_parishes=data['type_parishes']
    )
    await state.clear()

    await message.answer("Данные записаны", reply_markup=await kb.expense_arrival_keyboard())


@router.message(F.text == "Остатки")
async def remains_handler(message: Message):
    await message.answer("Остатки")
