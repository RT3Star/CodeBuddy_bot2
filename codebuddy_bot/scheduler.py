from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from database.models import SessionLocal, User
from utils.motivation import get_motivation
from datetime import datetime
import logging


async def send_daily_reminders(bot: Bot):
    db = SessionLocal()
    try:
        users = db.query(User).all()

        for user in users:
            if user.last_active:
                days = (datetime.utcnow() - user.last_active).days
                if days == 1:
                    try:
                        await bot.send_message(
                            chat_id=user.telegram_id,
                            text=f'💡 Не забувай про код! {get_motivation()}'
                        )
                    except Exception as e:
                        logging.warning(f"Не вдалося надіслати повідомлення {user.telegram_id}: {e}")

    except Exception as e:
        logging.error(f"Помилка в send_daily_reminders: {e}")
    finally:
        db.close()


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: send_daily_reminders(bot),
        trigger='cron',
        hour=9,
        minute=0
    )
    return scheduler