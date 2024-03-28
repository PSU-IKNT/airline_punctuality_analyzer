from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from repositories import AirRepository
router = APIRouter(
    tags=["Air"]
)

@router.get("/api/v2/airline_ratings_by_airports")
async def get_airline():
    airline_ratings = await AirRepository.get_flight_data()
    return {"airline_ratings": airline_ratings}

@router.get("/api/v2/overall_rating")
async def get_airline():
    airline_ratings = await AirRepository.get_overall_rating()
    return {"airline_ratings": airline_ratings}