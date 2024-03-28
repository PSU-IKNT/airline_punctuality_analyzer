from pydantic import BaseModel
from datetime import datetime

class AirlineOverAllRatingResponse(BaseModel):
    airlineIataCode: str
    totalFlights: int
    onTimeDepartures: int
    onTimeArrivals: int
    offTimeDepartures: int
    offTimeArrivals: int
    departureRating: float
    arrivalRating: float
    midRating: float
    ratingDate: datetime

class FlightData(BaseModel):
    jsonData: str