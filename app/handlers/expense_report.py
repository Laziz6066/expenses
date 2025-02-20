from datetime import datetime

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

import app.database.requests.expense as rq
from app.database.requests.requests import main_menu_back
from app.png import expense_png
from app.state import ReportExpenseState

expense_report_router = Router()


@expense_report_router.message(F.text == "Отчёт по расходам", StateFilter(default_state))
async def start_expense_report(message: Message, state: FSMContext):
    if await main_menu_back(message.text.strip(), state, message):
        return
    await state.set_state(ReportExpenseState.start_date)
    await message.answer("Выберите начальную дату:",
                         reply_markup=await SimpleCalendar().start_calendar())


@expense_report_router.callback_query(
    SimpleCalendarCallback.filter(),
    ReportExpenseState.start_date)
async def expense_start_date(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    selected_date = datetime(callback_data.year,
                             callback_data.month, callback_data.day)

    await state.update_data(start_date=selected_date)
    await state.set_state(ReportExpenseState.end_date)

    try:
        await callback_query.message.edit_text(
            "Теперь выберите конечную дату:",
            reply_markup=await SimpleCalendar().start_calendar()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback_query.message.answer(
                "Теперь выберите конечную дату:",
                reply_markup=await SimpleCalendar().start_calendar()
            )
        else:
            raise e


@expense_report_router.callback_query(
    SimpleCalendarCallback.filter(),
    ReportExpenseState.end_date)
async def expense_end_date(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    selected_date = datetime(callback_data.year,
                             callback_data.month, callback_data.day)
    data = await state.get_data()
    start_date = data['start_date']

    if selected_date < start_date:
        await callback_query.message.answer(
            "Ошибка! Конечная дата не может быть "
            "раньше начальной. Выберите заново.",
            reply_markup=await SimpleCalendar().start_calendar()
        )
        return

    expenses = await rq.get_expenses_by_date(
        start_date,
        selected_date,
        callback_query.from_user.id)

    # if expenses:
    #     report_text = "\n".join(str(exp) for exp in expenses)
    #     total_cash = sum(exp.amount for exp in expenses
    #                      if exp.type_expense.lower() == "наличными")
    #     total_plastic = sum(exp.amount for exp in expenses
    #                         if exp.type_expense.lower() == "пластик картой")
    #     total_overall = total_cash + total_plastic
    #     summary_text = (
    #         f"\n\nИтоги:\n"
    #         f"Наличными: {total_cash:,.0f} UZS\n"
    #         f"Пластик картой: {total_plastic:,.0f} UZS\n"
    #         f"Общий итог: {total_overall:,.0f} UZS"
    #     )
    # else:
    #     report_text = "Расходов за этот период нет."
    #     await callback_query.message.answer(report_text)

    # report_message = (
    #     f"Отчет по расходам с {start_date.strftime('%d.%m.%Y')} по "
    #     f"{selected_date.strftime('%d.%m.%Y')}:\n\n{report_text}{summary_text}"
    # )

    # await callback_query.message.answer(report_message)

    # Генерация PNG отчета, если есть данные
    if expenses:
        png_file_path = expense_png.generate_expense_png(
            expenses, start_date, selected_date)
        document = FSInputFile(png_file_path)
        await callback_query.message.answer_photo(photo=document)
    else:
        await callback_query.message.answer("Расходов за этот период нет.")
    await state.clear()
