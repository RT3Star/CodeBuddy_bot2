from database.models import Badge, UserBadge
from aiogram import Bot


async def check_and_award_badges(session, user, bot: Bot):
    earned = []
    if user.completed_tasks >= 10:
        earned.append("Task Slayer")
    if user.streak >= 5:
        earned.append("Streak Master")
    if user.streak >= 10:
        earned.append("Python Champion")

    async def award_badge(session, user, badge_name, bot: Bot):
        badge = session.query(Badge).filter(Badge.name == badge_name).first()
        if not badge:
            return False

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
                return True
            except Exception as e:
                print(f"Помилка відправки повідомлення про бейдж: {e}")
                return False

        return False

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


def check_topic_mastery(user, topic: str, session) -> str:

    try:
        completed_levels = session.query(UserBadge).filter(
            UserBadge.user_id == user.user_id,
        ).count()

        if completed_levels >= 3:
            return f"Майстер теми {topic}"
        return ""

    except Exception as e:
        print(f"Помилка перевірки mastery теми: {e}")
        return ""