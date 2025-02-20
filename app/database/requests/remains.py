from sqlalchemy import select

from app.database.models import Remains, async_session


async def get_remains(user_id: int):
    async with async_session() as session:
        result = await session.scalars(select(Remains)
                                       .where(Remains.user_id == user_id))
        return result.all()


async def get_remains_for_user(user_id: int):
    async with async_session() as session:
        result = await session.scalars(
            select(Remains).where(Remains.user_id == user_id)
        )
        return result.first()


async def update_remains(remains_obj: Remains):
    async with async_session() as session:
        # Обновляем запись
        await session.merge(remains_obj)
        await session.commit()
