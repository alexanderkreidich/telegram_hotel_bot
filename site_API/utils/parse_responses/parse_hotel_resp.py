from site_API.utils.requests.site_api_requests import get_locations_json, get_hotels_json, get_hotel_info_json


async def get_city_id(city: str) -> dict:
    city_id = dict()
    city = await get_locations_json(city=city, domain='US', locale='en_US')
    city_data = city['data']
    for data in city_data:
        if data['type'] == 'CITY':
            city = data['regionNames']['secondaryDisplayName']
            id_city = data['gaiaId']
            city_id[city] = id_city

    return city_id


async def hotel_info(hotel_id: str,  domain: str, locale: str):
    hotel_info_dict = dict()
    info = await get_hotel_info_json(domain=domain, locale=locale, hotel_id=hotel_id)
    hotel_info_dict["name"] = info['summary']['name']
    hotel_info_dict["address"] = info['summary']['location']['address']['addressLine']
    hotel_info_dict['Photo_1'] = info['propertyGallery']['images'][0]['image']['url']
    hotel_info_dict['Photo_2'] = info['propertyGallery']['images'][1]['image']['url']
    hotel_info_dict['Photo_3'] = info['propertyGallery']['images'][2]['image']['url']
    hotel_info_dict['stars'] = int(info['summary']['tagline'][:1]) * '⭐️'
    sub_title = info['summary']['map']['markers'][0]['subtitle']
    title = info['summary']['map']['markers'][0]['title']
    hotel_info_dict['map_mark'] = sub_title + 'from the airport on ' + title
    return hotel_info_dict



