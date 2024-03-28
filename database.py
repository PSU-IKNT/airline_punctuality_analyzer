from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.types import JSON

engine = create_async_engine(
    "sqlite+aiosqlite:///airline.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class AirlineOverAllRating(Base):
    __tablename__ = 'airline_overall_rating'

    id = Column(Integer, primary_key=True)
    airline_iata_code = Column(String)
    total_flights = Column(Integer)

    on_time_departures = Column(Integer)
    on_time_arrivals = Column(Integer)

    off_time_departures = Column(Integer)
    off_time_arrivals = Column(Integer)

    departure_rating = Column(Float)
    arrival_rating = Column(Float)

    mid_rating = Column(Float)

class FlightData(Base):
    __tablename__ = 'flight_data'

    id = Column(Integer, primary_key=True)
    json_data = Column(JSON)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
