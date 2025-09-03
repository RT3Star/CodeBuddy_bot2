from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from database.models import SessionLocal, User
import json
import os
import random

task_router = Router()

current_dir = os.path.dirname(os.path.abspath(__file__))
topic_tasks_path = os.path.join(current_dir, '..', 'data', 'topic_tasks.json')

try:
    with open(topic_tasks_path, 'r', encoding='utf-8') as f:
        TOPIC_TASKS = json.load(f)
    print(f"✅ Завантажено завдань для {len(TOPIC_TASKS)} тем")
except Exception as e:
    print(f"❌ Помилка завантаження topic_tasks.json: {e}")
    TOPIC_TASKS = {}


def get_task(topic=None, difficulty=None):
    if not TOPIC_TASKS:
        return None

    if not topic:
        topic = random.choice(list(TOPIC_TASKS.keys()))

    if topic not in TOPIC_TASKS:
        return None

    if not difficulty:
        difficulty = random.choice(list(TOPIC_TASKS[topic].keys()))

    if difficulty not in TOPIC_TASKS[topic] or not TOPIC_TASKS[topic][difficulty]:
        return None

    task = random.choice(TOPIC_TASKS[topic][difficulty])
    task['topic'] = topic
    task['difficulty'] = difficulty
    return task


@task_router.message(Command("task"))
async def send_task(message: Message, difficulty: str = None):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        topic = user.current_topic if user and user.current_topic else None
        task = get_task(topic, difficulty)

        if not task:
            await message.answer("❌ Не знайдено завдань з вказаними параметрами.")
            return

        buttons = []
        for i, opt in enumerate(task['options']):
            callback_data = f"task_{task['topic']}_{task['difficulty']}_{i}_{hash(str(task)) % 10000}"
            buttons.append([InlineKeyboardButton(text=opt, callback_data=callback_data)])

        text = (
            f"🎯 Тема: {task['topic']}\n"
            f"⚡ Складність: {task['difficulty']}\n\n"
            f"❓ {task['question']}\n\n"
        )

        if 'code' in task and task['code']:
            text += f"💻 Код:\n```python\n{task['code']}\n```"

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    except Exception as e:
        await message.answer("❌ Помилка при отриманні завдання")
        print(f"❌ Помилка: {e}")
    finally:
        db.close()


@task_router.message(Command("task_easy"))
async def send_easy_task(message: Message):
    await send_task(message, "easy")


@task_router.message(Command("task_medium"))
async def send_medium_task(message: Message):
    await send_task(message, "medium")


@task_router.message(Command("task_hard"))
async def send_hard_task(message: Message):
    await send_task(message, "hard")


@task_router.callback_query(F.data.startswith("task_"))
async def check_task_answer(query: CallbackQuery):
    await query.answer()

    db = SessionLocal()
    try:
        data_parts = query.data.split('_')
        topic = data_parts[1]
        difficulty = data_parts[2]
        selected = int(data_parts[3])

        task = None
        for t in TOPIC_TASKS[topic][difficulty]:
            if t['question'] in query.message.text:
                task = t
                break

        if not task:
            await query.message.answer("❌ Не вдалося знайти завдання для перевірки")
            return

        correct = task['answer']
        user_id = query.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if selected == correct:
            result = "✅ Правильно!"
            if user:
                user.xp += 10
                user.completed_tasks += 1
                db.commit()
        else:
            result = f"❌ Неправильно. Правильна відповідь: {task['options'][correct]}"

        explanation = f"📝 {task['explanation']}"

        if 'code' in task and task['code']:
            explanation += f"\n\n💻 Код:\n```python\n{task['code']}\n```"

        await query.message.edit_text(
            text=f"{result}\n\n{explanation}",
            parse_mode='Markdown',
            reply_markup=None
        )

    except Exception as e:
        await query.message.answer("❌ Помилка при перевірці відповіді")
        print(f"❌ Помилка: {e}")
    finally:
        db.close()