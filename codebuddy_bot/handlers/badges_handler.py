from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.orm import Session
from database.models import SessionLocal, UserBadge, Badge, User
from datetime import datetime, timedelta

badges_router = Router()


def has_badge(db: Session, user_id: int, badge_name: str) -> bool:
    badge = db.query(Badge).filter(Badge.name == badge_name).first()
    if not badge:
        return False

    user_badge = db.query(UserBadge).filter(
        UserBadge.user_id == user_id,
        UserBadge.badge_id == badge.badge_id
    ).first()

    return user_badge is not None


def award_badge(db: Session, user_id: int, badge_name: str, icon: str, description: str):
    badge = db.query(Badge).filter(Badge.name == badge_name).first()
    if not badge:
        badge = Badge(
            name=badge_name,
            icon=icon,
            description=description
        )
        db.add(badge)
        db.flush()

    if not has_badge(db, user_id, badge_name):
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge.badge_id
        )
        db.add(user_badge)
        db.commit()
        return True

    return False


@badges_router.message(F.text == "/badges")
async def badges_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()

        if not user_badges:
            msg = "🔍️ У тебе ще немає бейджів. Виконуй завдання, щоб їх заробити!"
        else:
            names = []
            for ub in user_badges:
                badge = db.query(Badge).filter(Badge.badge_id == ub.badge_id).first()
                if badge:
                    names.append(f"{badge.icon} {badge.name}")
            msg = "🔍️ Твої бейджі:\n" + "\n".join(names)

        await message.answer(msg)

    except Exception as e:
        await message.answer("✕ Сталася помилка при отриманні бейджів.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Vika")
async def vika_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "Знайшов ментора",
            "👩‍🏫",
            "Ви знайшли свого ментора Vika!"
        )
        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого ментора Vika! Отримано бейдж: 👩‍🏫 Знайшов ментора")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов свого ментора Vika раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Lyka")
async def Lyka_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Lyka",
            "👩‍🏫",
            "Ви знайшли свого одно групника Lyka!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Lyka! Отримано бейдж: 👩‍🏫 Знайти одно групника(Lyka)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Lyka раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Zhora")
async def Zhora_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Zhora",
            "👩‍🏫",
            "Ви знайшли свого одно групника Zhora!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Zhora! Отримано бейдж: 👩‍🏫 Знайти одно групника(Zhora)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Zhora раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()



@badges_router.message(F.text == "Nikita")
async def Nikita_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Nikita",
            "👩‍🏫",
            "Ви знайшли свого одно групника Nikita!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Nikita! Отримано бейдж: 👩‍🏫 Знайти одно групника(Nikita)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Nikita раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Ivan P")
async def IvanP_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Ivan P",
            "👩‍🏫",
            "Ви знайшли свого одно групника Ivan P.!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Ivan P.! Отримано бейдж: 👩‍🏫 Знайти одно групника(Ivan P.)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Ivan P. раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Kirill")
async def Kirill_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Kirill",
            "👩‍🏫",
            "Ви знайшли свого одно групника Kirill!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Kirill! Отримано бейдж: 👩‍🏫 Знайти одно групника(Kirill)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Kirill раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Nicole")
async def Nicole_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Nicole",
            "👩‍🏫",
            "Ви знайшли свого одно групника Nicole!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Nicole! Отримано бейдж: 👩‍🏫 Знайти одно групника(Nicole)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Nicole раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Dimitri")
async def Dimitri_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Dimitri",
            "👩‍🏫",
            "Ви знайшли свого одно групника Dimitri!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Dimitri! Отримано бейдж: 👩‍🏫 Знайти одно групника(Dimitri)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Dimitri раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Ivan A")
async def IvanA_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Ivan A",
            "👩‍🏫",
            "Ви знайшли свого одно групника Ivan A.!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Ivan A.! Отримано бейдж: 👩‍🏫 Знайти одно групника(Ivan A.)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Ivan A. раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Daniil")
async def Daniil_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Daniil",
            "👩‍🏫",
            "Ви знайшли свого одно групника Daniil!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Daniil! Отримано бейдж: 👩‍🏫 Знайти одно групника(Daniil)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Daniil раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "David")
async def Daniil_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника David",
            "👩‍🏫",
            "Ви знайшли свого одно групника David!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника David! Отримано бейдж: 👩‍🏫 Знайти одно групника(David)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов David раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Mykhailo")
async def Mykhailo_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Mykhailo",
            "👩‍🏫",
            "Ви знайшли свого одно групника Mykhailo!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Mykhailo! Отримано бейдж: 👩‍🏫 Знайти одно групника(Mykhailo)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Mykhailo раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Oleksandr")
async def Oleksandr_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Oleksandr",
            "👩‍🏫",
            "Ви знайшли свого одно групника Oleksandr!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Oleksandr! Отримано бейдж: 👩‍🏫 Знайти одно групника(Oleksandr)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Oleksandr раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()

@badges_router.message(F.text == "Katya")
async def Katya_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "ти знайшов одно групника Katya",
            "👩‍🏫",
            "Ви знайшли свого одно групника Katya!"
        )

        if awarded:
            await message.answer("🎉 Вітаю! Ти знайшов свого одно групника Katya! Отримано бейдж: 👩‍🏫 Знайти одно групника(Katya)")
        else:
            await message.answer("👩‍🏫 Ти вже знайшов Katya раніше!")

    except Exception as e:
        await message.answer("✗ Сталася помилка при видачі бейджа.")
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "Привіт")
async def hello_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "Перший крок",
            "👋",
            "Перше повідомлення в боті!"
        )

        if awarded:
            await message.answer("🎉 Привіт! Отримано бейдж: 👋 Перший крок")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message(F.text == "CodeBuddy")
async def secret_word_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id

        awarded = award_badge(
            db,
            user_id,
            "Секретний агент",
            "🕵️",
            "Знаєш секретне слово!"
        )

        if awarded:
            await message.answer("🎉 Ти знаєш секрет! Отримано бейдж: 🕵️ Секретний агент")
        else:
            await message.answer("🕵️ Ти вже знаєш наш секрет!")

    except Exception as e:
        await message.answer("✗ Сталася помилка.")
        print(f"Помилка: {e}")
    finally:
        db.close()


user_message_count = {}


@badges_router.message()
async def persistent_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        current_time = datetime.now()

        if user_id not in user_message_count:
            user_message_count[user_id] = []

        user_message_count[user_id].append(current_time)

        user_message_count[user_id] = [
            time for time in user_message_count[user_id]
            if current_time - time < timedelta(minutes=5)
        ]

        if len(user_message_count[user_id]) >= 3:
            awarded = award_badge(
                db,
                user_id,
                "Наполегливий",
                "💪",
                "Активна участь в бесіді!"
            )

            if awarded:
                await message.answer("🎉 Ти дуже активний! Отримано бейдж: 💪 Наполегливий")
                user_message_count[user_id] = []

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        db.close()


@badges_router.message()
async def night_owl_handler(message: Message):
    db = SessionLocal()
    try:
        user_id = message.from_user.id
        current_time = datetime.now()

        if 0 <= current_time.hour <= 6:
            awarded = award_badge(
                db,
                user_id,
                "Нічна сова",
                "🦉",
                "Активність в нічний час!"
            )

            if awarded:
                await message.answer("🎉 Нічна сова! Отримано бейдж: 🦉 Нічна сова")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        db.close()