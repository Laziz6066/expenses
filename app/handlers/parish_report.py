from datetime import datetime

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

import app.database.requests.parishes as rq
from app.png import parishe_png
from app.state import ReportParishState

parish_report_router = Router()


@parish_report_router.message(F.text == "Отчёт по приходам", StateFilter(default_state))
async def start_parish_report(message: Message, state: FSMContext):
    await state.set_state(ReportParishState.start_date)
    await message.answer("Выберите начальную дату:",
                         reply_markup=await SimpleCalendar().start_calendar())


@parish_report_router.callback_query(
    SimpleCalendarCallback.filter(),
    ReportParishState.start_date)
async def parish_start_date(callback_query: CallbackQuery,
                            callback_data: SimpleCalendarCallback,
                            state: FSMContext):
    selected_date = datetime(callback_data.year,
                             callback_data.month, callback_data.day)

    await state.update_data(start_date=selected_date)
    await state.set_state(ReportParishState.end_date)

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


@parish_report_router.callback_query(
    SimpleCalendarCallback.filter(),
    ReportParishState.end_date)
async def parish_end_date(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    selected_date = datetime(callback_data.year,
                             callback_data.month, callback_data.day)

    data = await state.get_data()
    start_date = data['start_date']

    if selected_date < start_date:
        await callback_query.message.answer(
            "Ошибка! Конечная дата не может "
            "быть раньше начальной. Выберите заново.",
            reply_markup=await SimpleCalendar().start_calendar()
        )
        return

    parishes = await rq.get_parishes_by_date(
        start_date,
        selected_date,
        callback_query.from_user.id)

    # if parishes:
    #     report_text = "\n".join(str(exp) for exp in parishes)
    # else:
    #     report_text = "Приходов за этот период нет."

    # await callback_query.message.answer(f"Отчёт по
    # приходам с {start_date.strftime('%d.%m.%Y')} по "
    # f"{selected_date.strftime('%d.%m.%Y')}:\n\n{report_text}")

    if parishes:
        png_file_path = parishe_png.generate_parish_png(
            parishes,
            start_date,
            selected_date)
        document = FSInputFile(png_file_path)
        await callback_query.message.answer_photo(photo=document)
    await state.clear()
