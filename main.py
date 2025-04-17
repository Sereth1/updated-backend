from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from router import user
from middleware import error_handler_middleware
from fastapi.middleware.cors import CORSMiddleware
from router.llm import llm_keys, llm_provider, llm_memory
from router.wallet import assets, wallet  

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Updated AI API",
    description="API for managing users, LLM memory, keys, wallets and more.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "User-related endpoints"},
        {"name": "LLM Providers", "description": "Available LLM API providers"},
        {"name": "LLM Keys", "description": "Store and manage API keys for various large language model providers"},
        {"name": "LLM Memory", "description": "Manage LLM-powered ideas, conversation messages, valuable information snippets, and custom memory collections to enhance context-aware interactions."},
        {"name": "Wallet", "description": "Wallet creation, crypto/fiat deposits, and user balances"},
        {"name": "Assets", "description": "Supported cryptocurrencies, tokens, and fiat currencies"},
    ]
)

# Add error handling middleware
app.middleware("http")(error_handler_middleware)

# Include routers with tags
app.include_router(user.router, tags=["Users"])
app.include_router(llm_provider.router, tags=["LLM Providers"])
app.include_router(llm_keys.router, tags=["LLM Keys"])
app.include_router(llm_memory.router, tags=["LLM Memory"])
app.include_router(wallet.router, tags=["Wallet"])
app.include_router(assets.router, tags=["Assets"])
