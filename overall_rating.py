import os
import json
from datetime import datetime
from database import AirlineOverAllRating
from repositories import AirRepository, FlightData
import aiohttp

class AirlineRatingCalculator:

    def __init__(self):
        self.rating_dataset = {}
        self.fly_data = {}

    async def add_flight(self, flight_data):

        airline_iata_code = flight_data["airlineIataCode"]

        if airline_iata_code not in self.rating_dataset:
            self.rating_dataset[airline_iata_code] = {
                "total_flights": 0,
                "on_time_departures": 0,
                "on_time_arrivals": 0
            }

        self.rating_dataset[airline_iata_code]["total_flights"] += 1

        plan_departure = datetime.fromisoformat(flight_data["planDeparture"])
        fact_departure = datetime.fromisoformat(flight_data["factDeparture"])

        plan_arrival = datetime.fromisoformat(flight_data["planArrival"])
        fact_arrival = datetime.fromisoformat(flight_data["factArrival"])

        departure_delay = (fact_departure - plan_departure).total_seconds() // 60
        arrival_delay = (fact_arrival - plan_arrival).total_seconds() // 60

        if departure_delay <= 15:
            self.rating_dataset[airline_iata_code]["on_time_departures"] += 1
        if arrival_delay <= 15:
            self.rating_dataset[airline_iata_code]["on_time_arrivals"] += 1

    async def add_rating_table(self):
        for airline_iata_code, data in self.rating_dataset.items():
            departure_rating = (data["on_time_departures"] / data["total_flights"]) * 100
            arrival_rating = (data["on_time_arrivals"] / data["total_flights"]) * 100
            new_rating = AirlineOverAllRating(

                airline_iata_code = airline_iata_code,
                total_flights = data["total_flights"],

                on_time_departures = data["on_time_departures"],
                on_time_arrivals = data["on_time_arrivals"],

                off_time_departures = data["total_flights"] - data["on_time_departures"],
                off_time_arrivals = data["total_flights"] - data["on_time_arrivals"],

                departure_rating = departure_rating,
                arrival_rating = arrival_rating,
                mid_rating = (departure_rating + arrival_rating) / 2,
            )
            await AirRepository.add_overall_rating(new_rating)
    async def add_flight_dataset(self, flight_data):

        departure_airport = flight_data["departureAirport"]
        arrival_airport = flight_data["arrivalAirport"]

        airline_iata_code = flight_data["airlineIataCode"]

        plan_departure = datetime.fromisoformat(flight_data["planDeparture"])
        fact_departure = datetime.fromisoformat(flight_data["factDeparture"])

        plan_arrival = datetime.fromisoformat(flight_data["planArrival"])
        fact_arrival = datetime.fromisoformat(flight_data["factArrival"])

        departure_delay = (fact_departure - plan_departure).total_seconds() // 60
        arrival_delay = (fact_arrival - plan_arrival).total_seconds() // 60


        if departure_airport not in self.fly_data:
            self.fly_data[departure_airport] = {}

        if arrival_airport not in self.fly_data:
            self.fly_data[arrival_airport] = {}


        if airline_iata_code not in self.fly_data[arrival_airport]:
            self.fly_data[arrival_airport][airline_iata_code] = {
                "total_flights": 0,
                "on_time_arrivals": 0,

            }

        self.fly_data[arrival_airport][airline_iata_code]["total_flights"] += 1

        if airline_iata_code not in self.fly_data[departure_airport]:
            self.fly_data[departure_airport][airline_iata_code] = {
                "total_flights": 0,
                "on_time_departures": 0,
            }

        self.fly_data[departure_airport][airline_iata_code]["total_flights"] += 1

        if 'on_time_departures' not in self.fly_data[departure_airport][airline_iata_code]:
            self.fly_data[departure_airport][airline_iata_code]["on_time_departures"] = 0

        if departure_delay <= 15:
            self.fly_data[departure_airport][airline_iata_code]["on_time_departures"] += 1

        if 'on_time_arrivals' not in self.fly_data[arrival_airport][airline_iata_code]:
            self.fly_data[arrival_airport][airline_iata_code]["on_time_arrivals"] = 0

        if arrival_delay <= 15:
            self.fly_data[arrival_airport][airline_iata_code]["on_time_arrivals"] += 1


    async def add_fly_data_json(self):
        json_dump = json.dumps(self.fly_data, indent=4)
        json_dump = json.loads(json_dump)
        new_dump = FlightData(json_data=json_dump)
        await AirRepository.add_flight_data(new_dump)

async def fetch_flight_data(page_number):
    url = f"http://85.193.81.44:8083/api/v1/flights?pageNumber={page_number}&pageSize=1000"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    if not data:
                        return None
                    return data
                except json.JSONDecodeError:
                    return None
            else:
                return None

calculator = AirlineRatingCalculator()

async def run_overall_rating():
    page_number = 0
    while True:
        flight_data_list = await fetch_flight_data(page_number)
        if flight_data_list is None:
            break

        for flight_data in flight_data_list:
            await calculator.add_flight(flight_data)
            await calculator.add_flight_dataset(flight_data)

        page_number += 1

    await calculator.add_rating_table()
    await calculator.add_fly_data_json()