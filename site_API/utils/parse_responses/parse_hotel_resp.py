from site_API.utils.requests.site_api_requests import get_locations_json, get_hotels_json, get_hotel_info_json


async def get_city_id(city: str, domain: str, locale: str) -> dict:
    city_id = ''
    city_country = city.split()
    city = await get_locations_json(city=city, domain=domain, locale=locale)
    city_data = city['data']
    for data in city_data:
        if data['type'] == 'CITY' and city_country[1] == data['regionNames']['secondaryDisplayName']:
            city_id = data['gaiaId']
            break

    return city_id


async def hotel_info(hotel_id: str, domain: str, locale: str):
    hotel_info_dict = dict()
    info = await get_hotel_info_json(domain=domain, locale=locale, hotel_id=hotel_id)
    hotel_info_dict["name"] = info['summary']['name']
    hotel_info_dict["address"] = info['summary']['location']['address']['addressLine']
    hotel_info_dict['Photo_1'] = info['propertyGallery']['images'][0]['image']['url']
    hotel_info_dict['Photo_2'] = info['propertyGallery']['images'][1]['image']['url']
    hotel_info_dict['Photo_3'] = info['propertyGallery']['images'][2]['image']['url']
    stars = info['summary']['tagline'][0]
    if isinstance(stars, int):
        hotel_info_dict['stars'] = int(info['summary']['tagline'][0]) * '⭐️'
    else:
        hotel_info_dict['stars'] = 'Информация не найдена'
    hotel_info_dict["time"] = info['summary']['map']['markers'][0]['subtitle'][:1]
    hotel_info_dict["title"] = info['summary']['map']['markers'][0]['title']
    return hotel_info_dict


async def get_hotels(domain: str, sort_order: str, locale: str, checkout_date: str, region_id: str,
                     adults_number: str, checkin_date: str):
    hotels = await get_hotels_json(domain=domain, sort_order=sort_order, locale=locale, checkout_date=checkout_date,
                                   region_id=region_id,
                                   adults_number=adults_number, checkin_date=checkin_date)
    return hotels
