from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from database.models import SessionLocal, User
import json
import os
import random

random_router = Router()

current_dir = os.path.dirname(os.path.abspath(__file__))
random_tasks_path = os.path.join(current_dir, '..', 'data', 'topic_tasks.json')

try:
    with open(random_tasks_path, "r", encoding="utf-8") as f:
        topic_tasks = json.load(f)
    print(f"✅ Завантажено завдань для {len(topic_tasks)} тем")
except Exception as e:
    print(f"❌ Помилка завантаження topic_tasks.json: {e}")
    topic_tasks = {}


def get_random_task(difficulty=None):
    all_tasks = []

    for topic, difficulties in topic_tasks.items():
        for diff_level, tasks in difficulties.items():
            if difficulty is None or diff_level == difficulty:
                for task in tasks:
                    task_with_meta = task.copy()
                    task_with_meta['topic'] = topic
                    task_with_meta['difficulty'] = diff_level
                    all_tasks.append(task_with_meta)

    if not all_tasks:
        return None

    return random.choice(all_tasks)


@random_router.message(Command("random_task"))
async def random_task_handler(message: Message):
    args = message.text.split()
    difficulty = None

    if len(args) > 1:
        diff = args[1].lower()
        if diff in ("easy", "medium", "hard"):
            difficulty = diff

    await send_random_task(message, difficulty)


@random_router.message(Command("random_easy"))
async def random_easy_handler(message: Message):
    await send_random_task(message, "easy")


@random_router.message(Command("random_medium"))
async def random_medium_handler(message: Message):
    await send_random_task(message, "medium")


@random_router.message(Command("random_hard"))
async def random_hard_handler(message: Message):
    await send_random_task(message, "hard")


async def send_random_task(message: Message, difficulty: str = None):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await message.answer("❌ Спочатку почни з /start")
            return

        task = get_random_task(difficulty)

        if not task:
            msg = "❌ Немає доступних завдань з такими параметрами."
            await message.answer(msg)
            return

        if 'options' in task:
            buttons = []
            for i, opt in enumerate(task['options']):
                button = InlineKeyboardButton(text=opt,
                                              callback_data=f"random_{task['topic']}_{task['difficulty']}_{i}")
                buttons.append([button])

            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        else:
            reply_markup = None

        msg = (
            f"🎲 Випадкове завдання:\n"
            f"📚 Тема: {task['topic']}\n"
            f"⚡ Складність: {task['difficulty']}\n\n"
            f"❓ {task['question']}\n\n"
        )

        if 'code' in task and task['code']:
            msg += f"💻 Код:\n```python\n{task['code']}\n```"

        await message.answer(
            msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    except Exception as e:
        await message.answer("❌ Сталася помилка при отриманні завдання")
        print(f"❌ Помилка: {e}")
    finally:
        db.close()


@random_router.callback_query(F.data.startswith("random_"))
async def random_callback_handler(query: CallbackQuery):
    await query.answer()

    db = SessionLocal()
    try:
        data_parts = query.data.split("_")
        if len(data_parts) < 4:
            await query.answer("❌ Помилка формату")
            return

        topic = data_parts[1]
        difficulty = data_parts[2]
        selected = int(data_parts[3])
        user_id = query.from_user.id

        user = db.query(User).filter(User.telegram_id == user_id).first()

        task = None
        if topic in topic_tasks and difficulty in topic_tasks[topic]:
            for t in topic_tasks[topic][difficulty]:
                if 'options' in t:
                    task = t
                    break

        if not task:
            await query.answer("❌ Завдання не знайдено")
            return

        correct = task['answer']

        if selected == correct:
            result = "✅ Правильно!"
            if user:
                user.xp += 5
                user.completed_tasks += 1
                db.commit()
        else:
            result = f"❌ Неправильно. Правильна відповідь: {task['options'][correct]}"

        explanation = f"📝 Пояснення: {task['explanation']}"

        if 'code' in task and task['code']:
            explanation += f"\n\n💻 Код:\n```python\n{task['code']}\n```"

        await query.message.edit_text(
            text=f"{result}\n\n{explanation}",
            parse_mode="Markdown",
            reply_markup=None
        )

    except Exception as e:
        await query.answer("❌ Помилка при обробці відповіді")
        print(f"❌ Помилка: {e}")
    finally:
        db.close()