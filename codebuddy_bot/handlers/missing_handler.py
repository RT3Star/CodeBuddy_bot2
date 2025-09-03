from aiogram.types import Message
from database.models import SessionLocal, User
from datetime import datetime, timedelta


async def missing(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await message.answer("❌ Спочатку почніть з /start")
            return

        today = datetime.utcnow().date()

        if user.daily_answered:
            last_answered_date = user.daily_answered.date()
            days_missing = (today - last_answered_date).days - 1

            if days_missing > 0:
                msg = f"📅 Ви пропустили щоденні завдання за останні {days_missing} дні(в)"
            else:
                msg = "✅ Ви не пропустили жодного щоденного завдання!"
        else:
            msg = "📅 Ви ще не починали щоденні завдання. Почніть з /daily"

        await message.answer(msg)

    except Exception as e:
        await message.answer("❌ Сталася помилка при перевірці пропущених завдань")
        print(f"Помилка: {e}")
    finally:
        db.close()


from aiogram import Router, F

missing_router = Router()


@missing_router.message(F.text == "/missing")
async def missing_handler(message: Message):
    await missing(message)