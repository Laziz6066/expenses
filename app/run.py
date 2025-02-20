import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.database.models import async_main
from app.handlers.exchange import exchange_router
from app.handlers.expense import expense_router
from app.handlers.expense_report import expense_report_router
from app.handlers.parish import parish_router
from app.handlers.parish_report import parish_report_router
from app.handlers.start import start_router


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(exchange_router)
    dp.include_router(expense_router)
    dp.include_router(expense_report_router)
    dp.include_router(parish_router)
    dp.include_router(parish_report_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
