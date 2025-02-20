from sqlalchemy.ext.asyncio import AsyncSession
import app.keyboards as kb
from app.database.models import async_session


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def main_menu_back(text, state, message):
    if text == "На главную":
        await state.clear()
        await message.answer(
            "Выберите нужную кнопку:",
            reply_markup=await kb.expense_arrival_keyboard()
        )
        return True  # сигнализируем о том, что обработка завершена
    return False


