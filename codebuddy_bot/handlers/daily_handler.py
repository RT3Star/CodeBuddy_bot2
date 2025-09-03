from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from database.models import SessionLocal, User
from datetime import datetime
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
questions_path = os.path.join(current_dir, '..', 'data', 'daily_questions.json')

if not os.path.exists(questions_path):
    print(f"❌ Файл не знайдено: {questions_path}")
    questions = []
else:
    try:
        with open(questions_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print(f"✅ Завантажено {len(questions)} питань")
    except Exception as e:
        print(f"❌ Помилка завантаження JSON: {e}")
        questions = []

daily_router = Router()


@daily_router.message(Command('daily'))
async def daily_handler(message: Message):
    print(f"🔔 Отримано /daily від user_id: {message.from_user.id}")

    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            print("❌ Користувач не знайдений в БД")
            await message.answer('❌ Спочатку почни з /start')
            return

        today = datetime.utcnow().date()
        print(f"📅 Сьогодні: {today}, остання відповідь: {user.daily_answered}")

        if user.daily_answered and user.daily_answered.date() == today:
            print("ℹ️ Користувач вже відповідав сьогодні")
            await message.answer('■ Ти вже відповідав на запитання сьогодні!')
            return

        if not questions:
            print("❌ Немає питань для завантаження")
            await message.answer('❌ Немає доступних питань')
            return

        q_index = user.streak % len(questions)
        q = questions[q_index]
        print(f"✅ Обрано питання ID: {q['id']}, індекс: {q_index}")

        buttons = []
        print(f"📋 Створено кнопки з callback_data:")
        for i, opt in enumerate(q['options']):
            callback_data = f"daily_{q['id']}_{i}"
            print(f"   {i}. {opt} → {callback_data}")
            buttons.append([InlineKeyboardButton(
                text=opt,
                callback_data=callback_data
            )])

        text = (
            f'■ Щоденне запитання:\n\n'
            f"{q['question']}\n\n"
            f"```python\n{q['code']}\n```"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        print("✅ Питання успішно відправлено")

    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        await message.answer("❌ Сталася помилка при завантаженні питання")
    finally:
        db.close()


@daily_router.callback_query(F.data.startswith('daily_'))
async def daily_callback_handler(query: CallbackQuery):
    print(f"🔔 Callback отримано: {query.data}")
    await query.answer()

    db = SessionLocal()
    try:
        data_parts = query.data.split('_')
        print(f"📊 Розділені дані: {data_parts}")

        if len(data_parts) < 3:
            print("❌ Неправильний формат callback_data")
            await query.answer("Помилка формату", show_alert=True)
            return

        qid = data_parts[1]
        selected = int(data_parts[2])
        user_id = query.from_user.id

        print(f"📊 ID питання: {qid}, обрано: {selected}, user: {user_id}")

        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            print("❌ Користувач не знайдений при обробці відповіді")
            await query.answer("Користувача не знайдено", show_alert=True)
            return

        q = None
        for question in questions:
            if str(question['id']) == qid:
                q = question
                break

        if not q:
            print(f"❌ Питання з ID {qid} не знайдено")
            await query.answer("Питання не знайдено", show_alert=True)
            return

        correct = q['answer']
        print(f"✅ Відповідь: обрано {selected}, правильно {correct}")

        if selected == correct:
            result = "✅ Правильно!"
            user.streak += 1
            user.xp += 10
            print(f"🎉 Правильно! Новий streak: {user.streak}, XP: {user.xp}")
        else:
            result = f"❌ Неправильно. Правильна відповідь: {q['options'][correct]}"
            user.streak = 0
            print(f"❌ Неправильно. Streak скинуто")

        user.daily_answered = datetime.utcnow()
        db.commit()
        print("✅ Дані користувача оновлено")

        explanation = (
            f"📝 Пояснення: {q['explanation']}\n\n"
            f"💻 Код:\n```python\n{q['code']}\n```"
        )

        await query.message.edit_text(
            text=f"{result}\n\n{explanation}",
            parse_mode='Markdown',
            reply_markup=None
        )
        print("✅ Відповідь оброблено успішно")

    except Exception as e:
        print(f"❌ Помилка при обробці callback: {e}")
        await query.answer("❌ Помилка при обробці відповіді", show_alert=True)
    finally:
        db.close()


@daily_router.message(Command("test_daily"))
async def test_daily(message: Message):
    print("🧪 Тестова команда test_daily викликана")
    await message.answer("✅ Daily handler працює! Тест пройдено")


@daily_router.message(Command("simple_test"))
async def simple_test(message: Message):
    button = InlineKeyboardButton(text="Натисни мене!", callback_data="simple_test_123")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Тест простих кнопок:", reply_markup=keyboard)
    print("🧪 Прості кнопки відправлено")


@daily_router.callback_query(F.data.startswith('simple_test_'))
async def simple_test_handler(query: CallbackQuery):
    await query.answer("✅ Кнопка працює!", show_alert=True)
    print(f"🎉 Проста кнопка спрацювала: {query.data}")