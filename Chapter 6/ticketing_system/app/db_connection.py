from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "sqlite+aiosqlite:///.database.db"
)

def get_engine():
    return create_async_engine(
            SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"timeout": 10}
    )

async def enable_wal():
    async with get_engine().begin() as conn:
        await conn.exec_driver_sql("PRAGMA journal_mode=WAL;")

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
