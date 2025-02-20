import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()
engine = create_async_engine(url=os.getenv('POSTGRESQL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(String(500))


class Parishes (Base):  # Приходы
    __tablename__ = "parishes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(500))
    amount: Mapped[int] = mapped_column()
    type_parishes: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now())

    def __str__(self):
        formatted_date = self.created_at.strftime("%d.%m.%Y %H:%M")
        return (f"{self.title} - {self.type_parishes} - {self.amount:,.0f}"
                f" UZS - {formatted_date}")


class Expenditure(Base):  # Расходование
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(500))
    amount: Mapped[int] = mapped_column()
    type_expense: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now())

    def __str__(self):
        formatted_date = self.created_at.strftime("%d.%m.%Y %H:%M")
        return (f"{self.title} - {self.type_expense} - {self.amount:,.0f}"
                f" UZS - {formatted_date}")


class Remains(Base):
    __tablename__ = 'remains'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    cash: Mapped[int] = mapped_column(nullable=True)
    plastic: Mapped[int] = mapped_column(nullable=True)

    def __str__(self):
        return (f"Наличные: {self.cash:,.0f} UZS\nКарта:"
                f" {self.plastic:,.0f} UZS")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
