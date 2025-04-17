from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from router import user
from middleware import error_handler_middleware
from fastapi.middleware.cors import CORSMiddleware
from router.llm import llm_idea, llm_message, llm_snippet, llm_collection
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
        {"name": "LLM Ideas", "description": "Store and manage high-level ideas or themes generated from LLM interactions."},
        {"name": "LLM Messages", "description": "Save and retrieve individual chat messages in an LLM session."},
        {"name": "LLM Snippets", "description": "Extracted useful information from chats or external sources."},
        {"name": "LLM Collections", "description": "Group useful snippets into collections for retrieval or reference."},
        {"name": "Wallet", "description": "Wallet creation, crypto/fiat deposits, and user balances"},
        {"name": "Assets", "description": "Supported cryptocurrencies, tokens, and fiat currencies"},
    ]
)

# Add error handling middleware
app.middleware("http")(error_handler_middleware)

# Include routers with tags
app.include_router(user.router, tags=["Users"])
app.include_router(llm_idea, tags=["LLM Ideas"])
app.include_router(llm_message, tags=["LLM Messages"])
app.include_router(llm_snippet, tags=["LLM Snippets"])
app.include_router(llm_collection, tags=["LLM Collections"])
app.include_router(wallet.router, tags=["Wallet"])
app.include_router(assets.router, tags=["Assets"])
