from datetime import datetime

from sqlalchemy import and_, select, update

from app.database.models import Parishes, Remains, async_session


async def get_parishes_by_date(
        start_date: datetime,
        end_date: datetime,
        user_id: int):
    async with async_session() as session:
        result = await session.scalars(
            select(Parishes).where(
                and_(
                    Parishes.user_id == user_id,
                    Parishes.created_at >= start_date,
                    Parishes.created_at <= end_date
                )
            )
        )
        return result.all()


async def add_parishes(
        title: str,
        amount: int,
        type_parishes: str,
        user_id: int):
    async with (async_session() as session):
        parishes = Parishes(
            title=title,
            amount=amount,
            type_parishes=type_parishes,
            user_id=user_id)
        session.add(parishes)

        stmt = None
        if type_parishes.lower() == "наличными":
            stmt = update(Remains).where(Remains.user_id == user_id
                                         ).values(cash=Remains.cash + amount)
        elif type_parishes.lower() == "пластик картой":
            stmt = update(Remains
                          ).where(Remains.user_id == user_id
                                  ).values(plastic=Remains.plastic + amount)

        if stmt is not None:
            result = await session.execute(stmt)
            if result.rowcount == 0:
                # Если записи для данного пользователя нет, создаём новую
                if type_parishes.lower() == "наличными":
                    remains = Remains(user_id=user_id, cash=amount, plastic=0)
                elif type_parishes.lower() == "пластик картой":
                    remains = Remains(user_id=user_id, cash=0, plastic=amount)
                session.add(remains)

        await session.commit()
