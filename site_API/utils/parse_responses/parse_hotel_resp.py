from site_API.utils.requests.site_api_requests import get_locations_json
import asyncio


async def get_cities_with_id(city: str) -> dict:
    cities_with_id = dict()
    cities = await get_locations_json(city=city)
    entities = cities.get('suggestions')[0]['entities']
    for elem in entities:
        city_name = elem.get('name')
        city_id = elem.get('destinationId')
        cities_with_id[city_name] = city_id

    return cities_with_id

city_dict = asyncio.run(get_cities_with_id('New York'))
for city, id_city in city_dict.items():
    print(city, id_city)

# async def get_hotels()


