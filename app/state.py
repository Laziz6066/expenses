from aiogram.fsm.state import State, StatesGroup


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


class ReportExpenseState(StatesGroup):
    start_date = State()
    end_date = State()


class ReportParishState(StatesGroup):
    start_date = State()
    end_date = State()


class ExchangeMoney(StatesGroup):
    direction = State()
    amount = State()
