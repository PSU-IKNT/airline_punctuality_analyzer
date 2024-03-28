from fastapi import FastAPI
from database import create_tables, drop_tables
from contextlib import asynccontextmanager
from routes import router
from overall_rating import run_overall_rating

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("tables dropped")
    await create_tables()
    print("tables created")
    await run_overall_rating()
    yield
    print("App OFF")

app = FastAPI(openapi_prefix="/api/v2/docs", lifespan=lifespan)
app.include_router(router)