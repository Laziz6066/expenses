from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import DateTime, func


load_dotenv()
engine = create_async_engine(url=os.getenv('POSTGRESQL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Parishes (Base):  # Приходы
    __tablename__ = "parishes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500))
    amount: Mapped[int] = mapped_column()
    type_parishes: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Expenditure(Base):  # Расходование
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500))
    amount: Mapped[int] = mapped_column()
    type_expense: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Remains(Base): # Остатки
    __tablename__ = 'remains'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cash: Mapped[int] = mapped_column()
    plastic: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
