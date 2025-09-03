import random
from database.models import Task


def get_random_task(session, difficulty=None, topic=None):
    query = session.query(Task)

    if difficulty:
        query = query.filter(Task.difficulty == difficulty)

    if topic:
        query = query.filter(Task.topic == topic)

    tasks = query.all()
    return random.choice(tasks) if tasks else None


def get_random_task_by_xp(session, user_xp):
    if user_xp < 50:
        difficulty = "easy"
    elif user_xp < 150:
        difficulty = "medium"
    else:
        difficulty = "hard"

    return get_random_task(session, difficulty=difficulty)


def get_random_topic_task(session, topic):
    difficulties = ["easy", "medium", "hard"]
    random.shuffle(difficulties)

    for difficulty in difficulties:
        task = get_random_task(session, difficulty=difficulty, topic=topic)
        if task:
            return task

    return None


def get_multiple_random_tasks(session, count=3, difficulty=None, topic=None):
    query = session.query(Task)

    if difficulty:
        query = query.filter(Task.difficulty == difficulty)

    if topic:
        query = query.filter(Task.topic == topic)

    tasks = query.all()

    if len(tasks) <= count:
        return tasks
    else:
        return random.sample(tasks, count)