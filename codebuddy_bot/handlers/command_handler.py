from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command


async def command(message: Message):
    keyboard = [
        [InlineKeyboardButton(text="📊 Прогрес", callback_data="progress")],
        [InlineKeyboardButton(text="🎖️ Бейджі", callback_data="badges")],
        [InlineKeyboardButton(text="🎲 Випадкове завдання", callback_data="random")],
        [InlineKeyboardButton(text="🏆 Лідерборд", callback_data="leaderboard")],
        [InlineKeyboardButton(text="🔄 Скинути", callback_data="reset")],
        [InlineKeyboardButton(text="✅ Завершити", callback_data="complete")],
        [InlineKeyboardButton(text="📈 Статистика", callback_data="stats")]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer(
        "🎮 Оберіть команду:",
        reply_markup=reply_markup
    )


from aiogram import Router

command_router = Router()


@command_router.message(Command("command"))
async def command_handler(message: Message):
    await command(message)