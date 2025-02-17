from app.models import async_session
from app.models import Expenditure, Remains, Parishes
from sqlalchemy import select
import logging
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_parishes():
    pass


async def get_expenses():
    pass


async def get_remains():
    pass


async def add_parishes(title: str, amount: int, type_parishes: str):
    async with async_session() as session:
        parishes = Parishes(title=title, amount=amount, type_parishes=type_parishes)
        session.add(parishes)
        await session.commit()


async def add_expenses(title: str, amount: int, type_expense: str):
    async with async_session() as session:
        expense = Expenditure(title=title, amount=amount, type_expense=type_expense)
        session.add(expense)
        await session.commit()


async def add_remains():
    pass
