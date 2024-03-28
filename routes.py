from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from repositories import AirRepository
from repositories import AirlineOverAllRating
from datetime import datetime, timedelta
from overall_rating import run_overall_rating
from database import create_tables, drop_tables
from schemas import AirlineOverAllRatingResponse, FlightData

router = APIRouter(
    tags=["Air"]
)

@router.get("/api/v2/airline_ratings_by_airports", response_description= "Successful Response Airline Ratings by Airports")
async def get_airline():
    airline_ratings = await AirRepository.get_flight_data()
    return {"airline_ratings": airline_ratings}

@router.get("/api/v2/overall_rating", response_description= "Successful Response Overall Rating")
async def get_airlines():
    last_update_date = await AirRepository.get_last_update_date()
    if last_update_date is not None:

        if datetime.now() - last_update_date > timedelta(days=1):
            print("data is up to date, start updating")
            await drop_tables()
            await create_tables()
            await run_overall_rating()
            print("data successfully updated")
    else:
        print("data not found start updating")
        await drop_tables()
        await create_tables()
        await run_overall_rating()
        print("data successfully updated")

    airline_ratings = await AirRepository.get_overall_rating()
    return {"airline_ratings": airline_ratings}