from datetime import datetime

from sqlalchemy import and_, select, update

from app.database.models import Expenditure, Remains, async_session


async def get_expenses_by_date(
        start_date: datetime,
        end_date: datetime,
        user_id: int
        ):
    async with async_session() as session:
        result = await session.scalars(
            select(Expenditure).where(
                and_(
                    Expenditure.user_id == user_id,
                    Expenditure.created_at >= start_date,
                    Expenditure.created_at <= end_date
                )
            )
        )
        return result.all()


async def add_expenses(title: str, amount: int, type_expense: str, user_id: int):
    async with async_session() as session:
        # Проверяем текущие остатки для пользователя
        remains_record = await session.scalar(
            select(Remains).where(Remains.user_id == user_id)
        )

        if type_expense.lower() == "наличными":
            current_funds = remains_record.cash if remains_record and remains_record.cash is not None else 0
        elif type_expense.lower() == "пластик картой":
            current_funds = remains_record.plastic if remains_record and remains_record.plastic is not None else 0
        else:
            current_funds = 0

        # Если средств недостаточно, возвращаем ошибку
        if current_funds < amount:
            return False, "Ошибка: недостаточно средств для расхода выбранным типом денег."

        # Записываем расход
        expense = Expenditure(
            title=title,
            amount=amount,
            type_expense=type_expense,
            user_id=user_id)
        session.add(expense)

        # Обновляем остатки в зависимости от типа расхода
        stmt = None
        if type_expense.lower() == "наличными":
            stmt = update(Remains).where(Remains.user_id == user_id).values(cash=Remains.cash - amount)
        elif type_expense.lower() == "пластик картой":
            stmt = update(Remains).where(Remains.user_id == user_id).values(plastic=Remains.plastic - amount)

        if stmt is not None:
            result = await session.execute(stmt)
            # Если записи остатков ещё нет, создаём её
            if result.rowcount == 0:
                if type_expense.lower() == "наличными":
                    remains_record = Remains(user_id=user_id, cash=-amount, plastic=0)
                elif type_expense.lower() == "пластик картой":
                    remains_record = Remains(user_id=user_id, cash=0, plastic=-amount)
                session.add(remains_record)

        await session.commit()
        return True, "Расход успешно записан."