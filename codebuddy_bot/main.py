import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start_handler import start_router
from handlers.help_handler import help_router
from handlers.topic_handler import topic_router
from handlers.task_handler import task_router
from handlers.progress_handler import progress_router
from handlers.leaderboard_handler import leaderboard_router
from handlers.mission_handler import mission_router
from handlers.daily_handler import daily_router
from handlers.random_handler import random_router
from handlers.reset_handler import reset_router
from handlers.user_handler import user_router
from handlers.badges_handler import badges_router

import config_local

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(
        token=config_local.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(topic_router)
    dp.include_router(task_router)
    dp.include_router(progress_router)
    dp.include_router(leaderboard_router)
    dp.include_router(mission_router)
    dp.include_router(daily_router)
    dp.include_router(random_router)
    dp.include_router(reset_router)
    dp.include_router(user_router)
    dp.include_router(badges_router)

    logger.info("Бот запускається...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())