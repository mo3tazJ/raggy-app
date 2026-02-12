from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


# 1. Define shared resources (e.g., db connections)
app_state = {}


# 2. Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("Starting up... loading resources")

    app_state["db"] = "Connected"
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  # type: ignore
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]  # type: ignore

    yield  # Control is yielded to FastAPI to start the app

    # --- Shutdown Logic ---
    print("Shutting down... cleaning up resources")
    app.mongo_conn.close()  # type: ignore
    app_state.clear()


# 3. Pass lifespan to the app
app = FastAPI(lifespan=lifespan)

# app = FastAPI() # Init app Without events

app.include_router(base.base_router)
app.include_router(data.data_router)
