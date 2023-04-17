import asyncio
from typing import Dict
import requests


async def make_response(url: str, params: dict, success=200):
    headers: dict = {"X-RapidAPI-Key": "18175e639emshb83b5ab1a6f004ep1ba319jsn299d3e3b84e0",
                     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

    response = requests.request(
        method="GET", url=url, headers=headers, params=params, timeout=3)

    status_code = response.status_code
    if status_code == success:
        return response.json()
    return status_code


async def get_locations_json(city: str) -> Dict:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": "en_US", "currency": "USD"}

    cities = await make_response(params=querystring, url=url)
    if isinstance(cities, int):
        raise Exception

    return cities


async def get_hotels_json(destinationId: str, pageNumber: str, pageSize: str, checkIn: str, checkOut: str,
                          adults1: str) -> Dict:
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destinationId, "pageNumber": pageNumber, "pageSize": pageSize, "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": adults1}

    response = await make_response(url=url, params=querystring)

    if isinstance(response, int):
        raise Exception

    return response


print(asyncio.run(
    get_hotels_json(destinationId='1506241', pageNumber='2', pageSize='25', checkIn='2023-07-01', checkOut='2023-07-10',
                    adults1='2')))


async def get_hotel_photos_json(hotel_id: str) -> Dict:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    response = await make_response(url=url, params=querystring)

    if isinstance(response, int):
        raise Exception

    return response
