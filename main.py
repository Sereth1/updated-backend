from fastapi import FastAPI
from database import engine, Base
from router import user  # <--- make sure this path is correct

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user.router)  # <--- this is what makes /users work
