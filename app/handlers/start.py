from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message, BufferedInputFile
from dotenv import load_dotenv
from openpyxl import Workbook
from io import BytesIO
from app.database.models import User
from sqlalchemy import select
import os
import app.database.requests.remains as remains_rq
import app.database.requests.requests as rq
import app.database.requests.users as user_rq
import app.keyboards as kb
from app.database.models import async_session
from app.png import remains_png

start_router = Router()
load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    async with rq.async_session() as session:
        user_exists = await user_rq.user_exists(message.from_user.id, session)

        if not user_exists:
            await user_rq.add_user(message.from_user.id,
                                   message.from_user.first_name, session)
    await message.answer("<b>К р а т к о е -- Р у к о в о д с т в о</b>\n"
                         "<b>Расход</b> - Записать расходы в книгу\n<b>Приход</b> - "
                         "Записать приходы в книгу\n<b>Обмен</b> - Обменять наличные на "
                         "пластик или наоборот (в книге)\n<b>Отчёт</b> - Посмотреть отчёты"
                         "\nВыберите нужную кнопку:",
                         reply_markup=await kb.expense_arrival_keyboard(),
                         parse_mode='html')


@start_router.message(F.text == "Отчёт")
async def report_handler(message: Message):
    await message.answer('Выберите нужный вам отчёт!',
                         reply_markup=await kb.expenses_report_keyboard())


@start_router.message(F.text == "Остатки")
async def remains_handler(message: Message):
    money = await remains_rq.get_remains(message.from_user.id)
    # remains_list = [str(remain) for remain in money]
    # await message.answer(f"{', '.join(remains_list)}")
    if money:
        png_file_path = remains_png.generate_remains_png(money)
        document = FSInputFile(png_file_path)
        await message.answer_photo(photo=document)


@start_router.message(F.text == "На главную")
async def main_menu(message: Message):
    await message.answer("Выберите нужную кнопку:",
                         reply_markup=await kb.expense_arrival_keyboard())


@start_router.message(Command("send_all"))
async def send_message_to_all_users(message: Message):
    if message.from_user.id != int(ADMIN_ID):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    async with (rq.async_session() as session):
        # Получаем список всех пользователей
        users = await user_rq.get_all_users(session)

        # Проверяем, есть ли фото в сообщении
        photo = message.photo[-1] if message.photo else None

        # Если есть фото, текст берём из caption
        # (если пользователь отправил фото с подписью)
        # Иначе — берём из message.text (после удаления команды /send_all)
        if photo:
            text_to_send = message.caption if message.caption else None
        else:
            text_to_send = message.text.replace("/send_all",
                                                "").strip() if message.text else None

        # Если нет ни текста, ни фото, выводим сообщение об ошибке
        if not text_to_send and not photo:
            await message.answer("Пожалуйста, добавьте текст или "
                                 "фото для отправки.")
            return

        # Отправляем сообщение каждому пользователю
        for user_id in users:
            try:
                if photo:
                    await message.bot.send_photo(
                        chat_id=user_id,
                        photo=photo.file_id,
                        caption=text_to_send[9:]
                    )
                else:
                    await message.bot.send_message(chat_id=user_id,
                                                   text=text_to_send[9:])
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю "
                      f"{user_id}: {e}")

        await message.answer("Сообщения отправлены всем пользователям.")


@start_router.message(Command("export_users"))
async def export_users_handler(message: Message):
    # Проверка, что пользователь является администратором
    if message.from_user.id != int(ADMIN_ID):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    # Получаем пользователей из БД
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    # Создаем Excel файл с помощью openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = "Пользователи"

    # Записываем заголовки столбцов
    ws.append(["ID", "Telegram ID", "User Name"])

    # Записываем данные пользователей
    for user in users:
        ws.append([user.id, user.tg_id, user.user_name])

    # Сохраняем Excel в буфер
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    # Создаем BufferedInputFile из BytesIO
    excel_file = BufferedInputFile(stream.getvalue(), filename="users.xlsx")

    # Отправляем файл пользователю
    await message.answer_document(document=excel_file)