from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv


load_dotenv()


async def expense_arrival_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='Расход'), KeyboardButton(text="Приход")],
        [KeyboardButton(text="Остатки"), KeyboardButton(text="Отчёт")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def expenses_report_keyboard():
    buttons = [
        [KeyboardButton(text='Расход за месяц'), KeyboardButton(text="Расход за неделю")],
        [KeyboardButton(text="Расход за день"), KeyboardButton(text="На главную")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def type_money():
    buttons = [
        [KeyboardButton(text='Наличными'), KeyboardButton(text="Пластик картой")],
        [KeyboardButton(text="На главную")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
