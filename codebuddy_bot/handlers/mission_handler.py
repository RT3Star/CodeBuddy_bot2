from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from database.models import SessionLocal, User
import random


async def mission(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await message.answer("❌ Спочатку почніть з /start")
            return

        missions = [
            "Напиши функцію, яка обчислює факторіал числа",
            "Створи клас для представлення користувача",
            "Напиши декоратор для вимірювання часу виконання функції",
            "Реалізуй алгоритм сортування бульбашкою",
            "Створи простий HTTP сервер на Python",
            "Напиши скрипт для парсингу веб-сторінки",
            "Реалізуй гру 'Вгадай число'",
            "Створи базу даних для зберігання завдань",
            "Напиши тести для своєї функції",
            "Оптимізуй існуючий код для покращення продуктивності"
        ]

        selected_mission = random.choice(missions)

        keyboard = [
            [InlineKeyboardButton(text="✅ Прийняти місію", callback_data="mission_accept")],
            [InlineKeyboardButton(text="🔁 Інша місія", callback_data="mission_another")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await message.answer(
            f"🎯 Місійне завдання:\n\n{selected_mission}",
            reply_markup=reply_markup
        )

    except Exception as e:
        await message.answer("❌ Сталася помилка при генерації місії")
        print(f"Помилка: {e}")
    finally:
        db.close()


async def handle_mission_callback(query: CallbackQuery):
    await query.answer()

    if query.data == "mission_accept":
        await query.message.answer("🎉 Місію прийнято! Успіхів у виконанні! 💪")
    elif query.data == "mission_another":
        await mission(query.message)


mission_router = Router()


@mission_router.message(F.text == "/mission")
async def mission_handler(message: Message):
    await mission(message)


@mission_router.callback_query(lambda c: c.data.startswith("mission_"))
async def mission_callback_handler(callback_query: CallbackQuery):
    await handle_mission_callback(callback_query)