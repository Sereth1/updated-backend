import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

# 🔥 HARD-CODED DATABASE URL (asyncpg!)
DATABASE_URL = "postgresql+asyncpg://testing_owner:npg_XkQntY0sMTB2@ep-hidden-sun-a94qd442-pooler.gwc.azure.neon.tech/testing?ssl=true"

print("🔌 DATABASE_URL =", DATABASE_URL)

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

async def main():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Connected!", result.scalar())
    except Exception as e:
        print("❌ Connection failed:", e)

asyncio.run(main())
