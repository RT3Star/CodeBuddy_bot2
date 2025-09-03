from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

async def help_command(message: Message):
    help_text = (
        "🆘 <b>CodeBuddy Help</b>\n\n"
        "📋 Доступні команди:\n"
        "/start - Почати роботу з ботом\n"
        "/badges - Переглянути здобуті бейджі\n"
        "/topic - Обрати або переглянути тему\n"
        "/progress - Перевірити свій прогрес\n"
        "/reset - Скинути прогрес або дані\n"
        "/leaderboard - Топ користувачів\n"
        "/random_task - Отримати випадкове завдання\n"
        "/daily - Щоденне питання\n"
        "/mission - Пропущені завдання\n"
        "/help - Допомога\n"
    )

    keyboard = [
        [KeyboardButton(text="/progress"), KeyboardButton(text="/badges")],
        [KeyboardButton(text="/random_task"), KeyboardButton(text="/leaderboard")],
        [KeyboardButton(text="/reset"), KeyboardButton(text="/stats")]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        help_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

from aiogram import Router, F

help_router = Router()

@help_router.message(Command("help"))
async def help_handler(message: Message):
    await help_command(message)