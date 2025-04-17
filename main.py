from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from router import llm_keys, user, llm_provider, wallet
from middleware import error_handler_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # App is ready
    # You could close resources here on shutdown

app = FastAPI(lifespan=lifespan)

# Add error handling middleware
app.middleware("http")(error_handler_middleware)

app.include_router(llm_keys.router)
app.include_router(user.router)
app.include_router(llm_provider.router)
app.include_router(wallet.router)