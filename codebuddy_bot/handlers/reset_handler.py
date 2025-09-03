from aiogram.types import Message
from aiogram.filters import Command
from database.models import SessionLocal, UserBadge, User


async def reset(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await message.answer("❌ Немає даних, щоб скинути.")
        else:
            user.completed_tasks = 0
            user.streak = 0
            user.xp = 0
            user.level = 1

            db.query(UserBadge).filter(UserBadge.user_id == user.user_id).delete()
            db.commit()

            await message.answer("✅ Статистика та бейджи скинуті. Починаємо з нуля! 🚀")

    except Exception as e:
        await message.answer("❌ Сталася помилка при скиданні даних")
        print(f"Помилка: {e}")
    finally:
        db.close()


from aiogram import Router, F

reset_router = Router()


@reset_router.message(F.text == "/reset")
async def reset_handler(message: Message):
    await reset(message)