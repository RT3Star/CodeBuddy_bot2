from database.models import User, SessionLocal
from datetime import datetime


def get_or_create_user(session, user_id, name=None, telegram_id=None):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(
            user_id=user_id,
            name=name or "",
            telegram_id=telegram_id or user_id,
            completed_tasks=0,
            streak=0,
            xp=0,
            level=1,
            last_active=datetime.utcnow()
        )
        session.add(user)
        session.commit()
    return user


def update_last_active(session, user):
    user.last_active = datetime.utcnow()
    session.commit()


def get_xp_for_difficulty(difficulty: str) -> int:
    return {'easy': 10, "medium": 20, "hard": 30}.get(difficulty, 0)


def add_xp_to_user(session, user, xp: int):
    user.xp = (user.xp or 0) + xp

    new_level = (user.xp // 100) + 1
    if new_level > user.level:
        user.level = new_level

    session.commit()
    return new_level > user.level


def get_user_by_telegram_id(session, telegram_id):
    return session.query(User).filter(User.telegram_id == telegram_id).first()


def reset_user_stats(session, user):
    user.completed_tasks = 0
    user.streak = 0
    user.xp = 0
    user.level = 1
    session.commit()


def get_user_progress(user):
    return {
        'completed_tasks': user.completed_tasks,
        'streak': user.streak,
        'xp': user.xp,
        'level': user.level,
        'last_active': user.last_active
    }