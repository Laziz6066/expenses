from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


async def add_user(user_id: int, user_name: str, session: AsyncSession):
    user = User(tg_id=user_id, user_name=user_name)
    session.add(user)
    await session.commit()


async def user_exists(user_id: int, session: AsyncSession) -> bool:
    result = await session.execute(select(User).filter_by(tg_id=user_id))
    return result.scalars().first() is not None


async def get_all_users(session: AsyncSession) -> list[int]:
    result = await session.execute(select(User.tg_id))
    return result.scalars().all()


