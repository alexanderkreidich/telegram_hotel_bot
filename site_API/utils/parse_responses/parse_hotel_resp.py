from site_API.utils.requests.site_api_requests import get_locations_json, get_hotels_json
import asyncio


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


city_id = asyncio.run(get_city_id('New York'))
for city, id_city in city_id.items():
    print(city, id_city)


async def hotel_info(domain: str, sort_order: str, locale: str, checkout_date: str, region_id: str,
                     adults_number: str, checkin_date: str):
    hotel_info_dict = dict()
    info = await get_hotels_json(domain=domain, locale=locale, checkin_date=checkin_date, checkout_date=checkout_date,
                                 region_id=region_id,
                                 adults_number=adults_number, sort_order=sort_order)
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


print()
hotel: dict = asyncio.run(hotel_info(domain='US', locale='en_US', checkin_date='2023-09-26', checkout_date='2023-09-27',
                                 region_id='2621',
                                 adults_number='1', sort_order='PRICE_LOW_TO_HIGH'))
for value, key in hotel.items():
    print(value, key)
