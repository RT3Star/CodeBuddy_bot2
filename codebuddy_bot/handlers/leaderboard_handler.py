from aiogram.types import Message
from database.models import SessionLocal, User


async def top(message: Message):
    db = SessionLocal()
    try:
        top_users = db.query(User).order_by(User.completed_tasks.desc()).limit(10).all()

        if not top_users:
            msg = "📊 Ніхто ще не виконав завдань."
        else:
            lines = ["🏆 Топ 10 користувачів:"]
            for i, user in enumerate(top_users, start=1):
                name = user.name or f"Користувач {user.user_id}"
                lines.append(f"{i}. {name} - {user.completed_tasks} завдань")
            msg = "\n".join(lines)

        await message.answer(msg)

    except Exception as e:
        await message.answer("❌ Сталася помилка при отриманні лідерборду")
        print(f"Помилка: {e}")
    finally:
        db.close()


from aiogram import Router, F

leaderboard_router = Router()


@leaderboard_router.message(F.text == "/leaderboard")
async def leaderboard_handler(message: Message):
    await top(message)