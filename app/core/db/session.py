import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Создаем движок для асинхронной работы с БД
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # True для отладки
    pool_pre_ping=True,
)

# Создаем фабрику сессий
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    """Dependency для FastAPI с обработкой ошибок."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()  # Автоматический commit
        except Exception:
            await session.rollback()  # Откат при ошибке
            raise
        finally:
            await session.close()  # Гарантированное закрытие

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass
