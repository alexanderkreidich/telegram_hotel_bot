from typing import Dict
import requests
from settings import SiteSettings

site = SiteSettings()


async def translate_text(text, from_lang, to_lang):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    payload = {
        "from": from_lang,
        "to": to_lang,
        "text": text
    }
    headers: dict = {"X-RapidAPI-Key": site.api_key_trans.get_secret_value(),
                     "X-RapidAPI-Host": site.host_api_trans.get_secret_value()}
    response = make_response_post(url, params=payload, headers=headers)
    if isinstance(response, int):
        raise Exception

    return response


async def make_response_post(url: str, params: dict, headers, success=200, ):
    response = requests.post(url, data=params, headers=headers)

    status_code = response.status_code
    if status_code == success:
        return response.json()
    return status_code


async def make_response(url: str, params: dict, success=200):
    headers: dict = {"X-RapidAPI-Key": site.api_key_hotels.get_secret_value(),
                     "X-RapidAPI-Host": site.host_api_hotels.get_secret_value()}

    response = requests.request(
        method="GET", url=url, headers=headers, params=params, timeout=10)

    status_code = response.status_code
    if status_code == success:
        return response.json()
    return status_code


async def get_locations_json(city: str, locale: str, domain: str) -> Dict:
    url = "https://worldwide-hotels.p.rapidapi.com/typeahead"

    payload = {
        "q": city,
        "language": "ru_RU"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "9394c6d853mshd73905c1e35aff2p10cc88jsn88d2c1997a2a",
        "X-RapidAPI-Host": "worldwide-hotels.p.rapidapi.com"
    }

    cities = await make_response_post(params=payload, url=url, headers=headers)

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


async def get_hotels_json(location_id: str):
    url = "https://worldwide-hotels.p.rapidapi.com/search"

    payload = {
        "location_id": location_id,
        "language": "ru_RU",
        "currency": "RUB",
        "offset": "0"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "9394c6d853mshd73905c1e35aff2p10cc88jsn88d2c1997a2a",
        "X-RapidAPI-Host": "worldwide-hotels.p.rapidapi.com"
    }

    response = await make_response_post(url=url, params=payload, headers=headers)

    if isinstance(response, int):
        raise Exception

    return response
