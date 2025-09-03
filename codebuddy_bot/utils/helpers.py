import os
import json
import random
from database.models import User


def get_task(topic: str, difficulty: str) -> dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "topic_tasks.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        tasks = data.get(topic, {}).get(difficulty, [])
        return random.choice(tasks) if tasks else {'question': '❌ Немає завдань для цієї теми та рівня.'}
    except Exception as e:
        return {'question': f'❌ Помилка при завантаженні завдань: {e}'}


def get_xp_for_difficulty(difficulty: str) -> int:
    return {'easy': 5, "medium": 10, "hard": 20}.get(difficulty, 0)


def add_xp_to_user(user, xp: int):
    user.xp = (user.xp or 0) + xp
    user.completed_tasks = (user.completed_tasks or 0) + 1


def update_user_stats(user):
    if not hasattr(user, 'completed_tasks'):
        user.completed_tasks = 0
    if not hasattr(user, 'xp'):
        user.xp = 0
    if not hasattr(user, 'streak'):
        user.streak = 0

    user.completed_tasks += 1
    user.xp += 10

    if hasattr(user, 'level'):
        user.level = (user.xp // 100) + 1



def get_user_progress(user) -> dict:
    return {
        'completed_tasks': getattr(user, 'completed_tasks', 0),
        'xp': getattr(user, 'xp', 0),
        'streak': getattr(user, 'streak', 0),
        'level': getattr(user, 'level', 1),
        'current_topic': getattr(user, 'current_topic', '')
    }


def can_user_complete_daily(user) -> bool:
    from datetime import datetime
    if not hasattr(user, 'daily_answered') or not user.daily_answered:
        return True
    return datetime.utcnow().date() > user.daily_answered.date()