from aiogram.fsm.state import StatesGroup, State


class AddParishes(StatesGroup):
    title = State()
    amount = State()
    type_parishes = State()


class AddExpenditure(StatesGroup):
    title = State()
    amount = State()
    type_expense = State()


class AddRemains(StatesGroup):
    cash = State()
    plastic = State()
