from site_API.utils.requests.site_api_requests import get_locations_json


async def get_city_id(city: str) -> dict:
    city, country = city.split()
    inp = city + ' ' + country
    data = await get_locations_json(city=inp)
    for entry in data['results']['data']:
        if entry['result_object'].get('name') == city and entry['result_object'].get('location_string').endswith(country):
            return entry['result_object']['location_id']



