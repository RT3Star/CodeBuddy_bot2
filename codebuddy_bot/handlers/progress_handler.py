from aiogram.types import Message
from database.models import SessionLocal, User


async def progress(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            msg = "❌ У вас немає прогресу. Виконуйте завдання для його отримання."
        else:
            msg = (
                "📊 Твій прогрес:\n"
                f"🎯 Тема: {user.current_topic or 'не вибрано'}\n"
                f"✅ Завдань виконано: {user.completed_tasks}\n"
                f"🔥 Серія: {user.streak} днів\n"
                f"⭐ XP: {user.xp}\n"
                f"📈 Рівень: {user.level}"
            )

        await message.answer(msg)

    except Exception as e:
        await message.answer("❌ Сталася помилка при отриманні прогресу")
        print(f"Помилка: {e}")
    finally:
        db.close()


from aiogram import Router, F

progress_router = Router()


@progress_router.message(F.text == "/progress")
async def progress_handler(message: Message):
    await progress(message)