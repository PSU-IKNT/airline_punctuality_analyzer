import json
from database import new_session, AirlineOverAllRating, FlightData
from sqlalchemy import select

class AirRepository:

    @classmethod
    async def add_overall_rating(cls, data: AirlineOverAllRating):
        async with new_session() as session:
            session.add(data)
            await session.commit()

    @classmethod
    async def add_flight_data(cls, data: FlightData):
        async with new_session() as session:
            session.add(data)
            await session.commit()

    @classmethod
    async def get_overall_rating(cls):
        async with new_session() as session:
            query = select(AirlineOverAllRating)
            result = await session.execute(query)
            data = result.scalars().all()
            return data

    @classmethod
    async def get_flight_data(cls):
        async with new_session() as session:
            query = select(FlightData)
            result = await session.execute(query)
            entry = result.scalars().all()
            print(entry)
            return entry