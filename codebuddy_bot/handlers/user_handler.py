from aiogram.types import Message
from database.models import Badge, UserBadge, User, SessionLocal
from aiogram import Bot


async def check_and_award_badges(session, user, bot: Bot):
    earned = []
    if user.completed_tasks >= 10:
        earned.append("Task Slayer")
    if user.streak >= 5:
        earned.append("Streak Master")
    if user.streak >= 10:
        earned.append("Python Champion")

    for name in earned:
        badge = session.query(Badge).filter(Badge.name == name).first()
        if not badge:
            continue

        exists = session.query(UserBadge).filter(
            UserBadge.user_id == user.user_id,
            UserBadge.badge_id == badge.badge_id
        ).first()

        if not exists:
            ub = UserBadge(user_id=user.user_id, badge_id=badge.badge_id)
            session.add(ub)
            session.commit()

            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"🎉 Вітаю! Ти отримав новий бейдж: *{badge.name}*",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Помилка відправки повідомлення про бейдж: {e}")


async def get_user_stats(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await message.answer("❌ Користувача не знайдено. Почніть з /start")
            return

        stats_text = (
            f"📊 Статистика користувача:\n"
            f"🆔 ID: {user.user_id}\n"
            f"👤 Ім'я: {user.name or 'Не вказано'}\n"
            f"✅ Виконано завдань: {user.completed_tasks}\n"
            f"🔥 Серія: {user.streak} днів\n"
            f"⭐ XP: {user.xp}\n"
            f"📈 Рівень: {user.level}\n"
            f"🎯 Поточна тема: {user.current_topic or 'Не обрана'}"
        )

        await message.answer(stats_text)

    except Exception as e:
        await message.answer("❌ Помилка при отриманні статистики")
        print(f"Помилка: {e}")
    finally:
        db.close()


from aiogram import Router, F

user_router = Router()


@user_router.message(F.text == "/user_stats")
async def user_stats_handler(message: Message):
    await get_user_stats(message)