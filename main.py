from fastapi import FastAPI
from database import create_tables, drop_tables
from contextlib import asynccontextmanager
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("App OFF")
    yield

description = """
# AviaRatingAnalysisAPI - быстрый инструмент для анализа больших объемов данных
# и выстраивания рейтинга мировых авиакомпаний🚀

## Возможности
### - Построение рейтинга авиакомпаний на основе задержанных рейсов из дампов вашей базы данных
### - Определение количества рейсов конкретных авиакомпаний в заданном аэропорту и их процент успешного выполнения
"""

app = FastAPI(openapi_prefix="/api/v2/docs", lifespan=lifespan,
              title="AviaRatingAnalysisAPI",
    description=description,
    version="0.0.1",
    license_info={
        "name": "NGINX DOCS",
        "url": "https://nginx.org/en/docs/",
    })
app.include_router(router)