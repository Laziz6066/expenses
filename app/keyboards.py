from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()


async def expense_arrival_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='Расход'), KeyboardButton(text="Приход")],
        [KeyboardButton(text="Обмен"), KeyboardButton(text="Отчёт")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def expenses_report_keyboard():
    buttons = [
        [KeyboardButton(text='Отчёт по расходам'),
         KeyboardButton(text="Отчёт по приходам")],
        [KeyboardButton(text="Остатки"), KeyboardButton(text="На главную")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def type_money():
    buttons = [
        [KeyboardButton(text='Наличными'),
         KeyboardButton(text="Пластик картой")],
        [KeyboardButton(text="На главную")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def exchange_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='Плас. -> Нал.')],
        [KeyboardButton(text="Нал. -> Плас")],
        [KeyboardButton(text="На главную")]]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
