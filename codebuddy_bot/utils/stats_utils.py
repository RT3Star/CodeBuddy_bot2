from database.models import User, SessionLocal
from datetime import datetime


def update_user_stats(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None

    user.completed_tasks += 1

    if user.last_active:
        days_diff = (datetime.utcnow() - user.last_active).days
        if days_diff == 1:
            user.streak += 1
        elif days_diff > 1:
            user.streak = 1
    else:
        user.streak = 1

    user.last_active = datetime.utcnow()
    session.commit()
    return user


def calculate_level(xp: int) -> int:
    return (xp // 100) + 1


def get_xp_for_next_level(current_level: int) -> int:
    return current_level * 100


def update_user_xp(session, user_id, xp_earned):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None

    user.xp = (user.xp or 0) + xp_earned
    new_level = calculate_level(user.xp)

    level_up = False
    if hasattr(user, 'level') and new_level > user.level:
        user.level = new_level
        level_up = True

    session.commit()
    return user, level_up


def get_user_rank(session, user_id):
    users = session.query(User).order_by(User.xp.desc()).all()
    for rank, user in enumerate(users, start=1):
        if user.user_id == user_id:
            return rank
    return None