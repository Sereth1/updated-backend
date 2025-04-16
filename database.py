from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://testing_owner:npg_XkQntY0sMTB2@ep-hidden-sun-a94qd442-pooler.gwc.azure.neon.tech/testing"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
