from typing import Dict
import requests
import asyncio


async def _make_response(url: str, params: dict, success=200):
    headers: dict = {"X-RapidAPI-Key": "18175e639emshb83b5ab1a6f004ep1ba319jsn299d3e3b84e0",
                     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

    response = requests.request(
        method="GET", url=url, headers=headers, params=params, timeout=3)

    status_code = response.status_code
    response = await response.json()
    if status_code == success:
        return response
    return status_code


async def _get_locations(city: str) -> Dict:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}

    cities = await _make_response(params=querystring, url=url)
    if isinstance(cities, int):
        raise Exception

    return cities


city_dict = _get_locations(city='moscow')
asyncio.run(city_dict)
