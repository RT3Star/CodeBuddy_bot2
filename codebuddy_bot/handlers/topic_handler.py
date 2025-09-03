from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.models import SessionLocal, User
import json
import os

topic_router = Router()

current_dir = os.path.dirname(os.path.abspath(__file__))
topics_path = os.path.join(current_dir, '..', 'data', 'topics.json')
topic_tasks_path = os.path.join(current_dir, '..', 'data', 'topic_tasks.json')

try:
    with open(topics_path, 'r', encoding='utf-8') as f:
        TOPICS = json.load(f)
    print(f"✅ Завантажено {len(TOPICS)} тем")
except Exception as e:
    print(f"❌ Помилка завантаження topics.json: {e}")
    TOPICS = ["Lambda", "List comprehension", "Decorators"]

try:
    with open(topic_tasks_path, 'r', encoding='utf-8') as f:
        TOPIC_TASKS = json.load(f)
    print(f"✅ Завантажено завдань для {len(TOPIC_TASKS)} тем")
except Exception as e:
    print(f"❌ Помилка завантаження topic_tasks.json: {e}")
    TOPIC_TASKS = {}


@topic_router.message(Command("topics"))
async def show_topics(message: Message, state: FSMContext):
    keyboard = []
    for topic in TOPICS:
        keyboard.append([InlineKeyboardButton(text=topic, callback_data=f"topic:{topic}")])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = "📚 Оберіть тему:\n\n"
    for i, topic in enumerate(TOPICS, 1):
        text += f"{i}. {topic}\n"

    await message.answer(text, reply_markup=reply_markup)


@topic_router.message(Command("topic"))
async def topic_command(message: Message):
    await show_topics(message, state=None)


@topic_router.callback_query(F.data.startswith("topic:"))
async def topic_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    topic = callback.data.split(':', 1)[1]

    db = SessionLocal()
    try:
        user_id = callback.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user:
            user.current_topic = topic
            db.commit()
            print(f"✅ Користувач {user_id} обрав тему: {topic}")
    except Exception as e:
        print(f"❌ Помилка збереження теми: {e}")
    finally:
        db.close()

    if topic in TOPIC_TASKS:
        task_count = sum(len(tasks) for tasks in TOPIC_TASKS[topic].values())
        message_text = (
            f"🎯 Тема \"{topic}\" обрана!\n\n"
            f"📊 Доступно завдань: {task_count}\n\n"
            f"Для отримання завдань цієї теми:\n"
            f"• /task - випадкове завдання\n"
            f"• /task_easy - легкі завдання\n"
            f"• /task_medium - середні завдання\n"
            f"• /task_hard - складні завдання"
        )
    else:
        message_text = (
            f"🎯 Тема \"{topic}\" обрана!\n\n"
            f"⚠️ Наразі немає завдань для цієї теми.\n"
            f"Спробуйте обрати іншу тему за допомогою /topics"
        )

    await callback.message.answer(message_text)


@topic_router.message(Command("current_topic"))
async def current_topic(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if user and user.current_topic:
            topic = user.current_topic
            if topic in TOPIC_TASKS:
                task_count = sum(len(tasks) for tasks in TOPIC_TASKS[topic].values())
                response = (
                    f"📊 Поточна тема: {topic}\n"
                    f"🔢 Доступно завдань: {task_count}\n\n"
                    f"Для роботи з завданнями:\n"
                    f"• /task - випадкове завдання\n"
                    f"• /task_easy - легкі завдання\n"
                    f"• /task_medium - середні завдання\n"
                    f"• /task_hard - складні завдання\n\n"
                    f"Щоб змінити тему: /topics"
                )
            else:
                response = (
                    f"📊 Поточна тема: {topic}\n\n"
                    f"⚠️ Наразі немає завдань для цієї теми.\n"
                    f"Щоб змінити тему: /topics"
                )
        else:
            response = (
                "📊 Ви ще не обрали тему.\n\n"
                "Оберіть тему за допомогою /topics"
            )

        await message.answer(response)
    except Exception as e:
        await message.answer("❌ Помилка при отриманні поточної теми")
        print(f"❌ Помилка: {e}")
    finally:
        db.close()