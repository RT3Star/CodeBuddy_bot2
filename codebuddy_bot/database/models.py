from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from codebuddy_bot.config_local import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, default='')
    avatar = Column(String, default='')
    last_active = Column(DateTime, default=datetime.utcnow)
    streak = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    current_topic = Column(String, default='')
    badges = Column(String, default='')
    xp = Column(Integer, default=0)
    daily_answered = Column(DateTime, default=None)
    level = Column(Integer, default=1)


class Badge(Base):
    __tablename__ = 'badges'
    badge_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)


class UserBadge(Base):
    __tablename__ = 'user_badges'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    badge_id = Column(Integer, ForeignKey('badges.badge_id'))


class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    topic = Column(String)
    difficulty = Column(String)
    content = Column(String)


Base.metadata.create_all(engine)