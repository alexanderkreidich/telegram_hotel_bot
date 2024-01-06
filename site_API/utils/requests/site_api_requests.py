from typing import Dict
import requests
from settings import SiteSettings

site = SiteSettings()


async def make_response(url: str, params: dict, success=200):
    headers: dict = {"X-RapidAPI-Key": site.api_key.get_secret_value(),
                     "X-RapidAPI-Host": site.host_api.get_secret_value()}

    response = requests.request(
        method="GET", url=url, headers=headers, params=params, timeout=10)

    status_code = response.status_code
    if status_code == success:
        return response.json()
    return status_code


async def get_locations_json(city: str, locale: str, domain: str) -> Dict:
    url = "https://hotels-com-provider.p.rapidapi.com/v2/regions"
    querystring = {"locale": locale, "query": city, "domain": domain}

    cities = await make_response(params=querystring, url=url)

    if isinstance(cities, int):
        raise Exception

    return cities


async def get_hotel_info_json(domain: str, locale: str, hotel_id: str) -> Dict:
    url = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/details"

    querystring = {"domain": domain, "locale": locale, "hotel_id": hotel_id}

    response = await make_response(url=url, params=querystring)

    if isinstance(response, int):
        raise Exception

    return response


async def get_hotels_json(domain: str, sort_order: str, locale: str, checkout_date: str, region_id: str,
                          adults_number: str, checkin_date: str):
    url = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search"
    querystring = {"domain": domain, "sort_order": sort_order, "locale": locale, "checkout_date": checkout_date,
                   "region_id": region_id, "adults_number": adults_number, "checkin_date": checkin_date, 'lodging_type': 'HOTEL'}

    response = await make_response(url=url, params=querystring)

    if isinstance(response, int):
        raise Exception

    return response

