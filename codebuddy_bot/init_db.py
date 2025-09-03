from codebuddy_bot.database.models import Base, engine

if __name__ == "__main__":
    print(f"🔄 Dropping & recreating tables for: {engine.url}")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables recreated!")
