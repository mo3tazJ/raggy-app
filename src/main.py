from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory


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

    # Initialize LLM Provider Factory and store in app state
    llm_provider_factory = LLMProviderFactory(config=settings)  # type: ignore
    app_state["llm_provider_factory"] = llm_provider_factory

    # Initialize vectordb Provider Factory and store in app state
    vectordb_provider_factory = VectorDBProviderFactory(config=settings)
    app_state["vectordb_provider_factory"] = vectordb_provider_factory

    # Create and configure generation client
    generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND)
    generation_client.set_generation_model(
        model_id=settings.GENERATION_MODEL_ID)
    app_state["generation_client"] = generation_client
    app.generation_client = generation_client  # type: ignore

    # Create and configure embedding client
    embedding_client = llm_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND)
    embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID, embedding_size=settings.EMBEDDING_MODEL_SIZE)
    app_state["embedding_client"] = embedding_client
    app.embedding_client = embedding_client  # type: ignore

    # Create and configure vectordb client
    vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client = vectordb_client
    app_state["vectordb_client"] = vectordb_client
    app.vectordb_client.connect()  # type: ignore

    yield  # Control is yielded to FastAPI to start the app

    # --- Shutdown Logic ---
    print("Shutting down... cleaning up resources")
    app.mongo_conn.close()  # type: ignore
    app.vectordb_client.disconnect()  # type: ignore
    app_state.clear()

# 3. Pass lifespan to the app
app = FastAPI(lifespan=lifespan)  # type: ignore


# # Init app Without events using lifespan, we will handle startup and shutdown events separately
# app = FastAPI()
# async def startup_function():
#     print("Starting up... loading resources")
# async def shutdown_function():
#     print("Shutting down... cleaning up resources")

# app.router.lifespan.on_startup.append(startup_function)
# app.router.lifespan.on_shutdown.append(shutdown_function)

app.include_router(base.base_router)
app.include_router(data.data_router)
