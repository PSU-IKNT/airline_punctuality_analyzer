from fastapi import FastAPI
from database import create_tables, drop_tables
from contextlib import asynccontextmanager
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("App OFF")
    yield

app = FastAPI(openapi_prefix="/api/v2/docs", lifespan=lifespan)
app.include_router(router)