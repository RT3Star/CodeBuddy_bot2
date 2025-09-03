from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

def get_or_create_user(user):
    print(f"Користувач {user.first_name} запустив бота")
    return {"id": user.id, "name": user.first_name}

@start_router.message(Command("start"))
async def start_command(message: types.Message):
    user = get_or_create_user(message.from_user)
    await message.answer(
        f"👋 Вітаю, {user['name']}!\n\n"
        "Я — CodeBuddy, твій помічник у вивченні Python!\n\n"
        "🚀 Ось що я вмію:\n"
        "• /topic - Обрати тему для вивчення\n"
        "• /random_task - Отримати завдання\n" 
        "• /help - Отримати більше команди\n\n"
        "Починаймо навчання! 🐍"
    )