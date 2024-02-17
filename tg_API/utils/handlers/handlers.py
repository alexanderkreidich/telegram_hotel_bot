# TODO  заменить домейн и локал на страны беларусь, грузия, казахстан, абхазия
# Изменить кнопку хай чтобы город выбирался уже после ее нажатия
# сделать кнопку low
# добаввить адрес отеля и ссылку на карты, чтобы можно было сразу построить маршрут 
import aiogram
from database.common.models import save_search, get_user_search_history, format_search_history
from tg_API.utils.states.state import States
from load_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types, utils
from site_API.utils.parse_responses.parse_hotel_resp import get_city_id
from tg_API.utils.keyboards.keyboards import get_kb_commands, domains, commands, locales
import re
from site_API.utils.requests.site_api_requests import get_hotels_json
help_text = """
Команды:
● /help — помощь по командам бота;
● /low — вывод минимальных показателей (с изображением товара/услуги/и так
далее);
● /high — вывод максимальных (с изображением товара/услуги/и так далее);
● /custom — вывод показателей пользовательского диапазона (с изображением
товара/услуги/и так далее);
/history — вывод истории запросов пользователей.
"""


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в KickSwitchHotels! Это телеграмм-бот,'
                              ' для поиска отелей по оптимальной цене!'
                              ' Надеюсь этот бот будет для вас полезным!')
    await message.answer(text='Выберите команду', reply_markup=get_kb_commands(commands))
    await States.wait_command.set()


@dp.message_handler(state=States.wait_command, commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=help_text, reply_markup=get_kb_commands(commands))


@dp.message_handler(commands=['Вернуться в меню'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await States.wait_command.set()
    await message.reply('Операция отменена.')


# LOW COMMAND

@dp.message_handler(commands=['low'], state=States.wait_command)
async def cmd_low(message: types.Message):
    await States.country.set()
    await message.reply("В какую страну вы хотели бы полететь?")


@dp.message_handler(state=States.country)
async def process_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await States.city.set()
    await message.reply("Какой город в этой стране вы хотите посетить?")


@dp.message_handler(state=States.city)
async def choice_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.capitalize()
        inp = data['city'] + ' ' + data['country']
        data['city_id'] = await get_city_id(city=inp, domain=domains, locale=locales)
        if data['city_id']:
            await message.answer(text='City_id is okay')

    await message.answer(text='Сколько вариантов отелей вам отправить?')
    await States.hotel_count.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=States.hotel_count)
async def process_hotel_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hotel_count'] = int(message.text)
        hotels = await get_hotels_json(data['city_id'])
        elements = []
        for elem in hotels['results']['data']:
            if elem.get('price', '') != '':
                elements.append(elem)

        # Проверяем, что все элементы в filtered_data имеют 'price'
        all_have_price = all('price' in elem and elem['price'] != '' for elem in elements)

        if all_have_price:
            print("Все элементы в filtered_data имеют 'price'")
            hotels['results']['data'] = elements
        else:
            print("Некоторые элементы в filtered_data не имеют 'price'")

        # Function to extract numerical price from the price string
        def get_price(element):
            print(element.get('price', '').split())
            price_str = element.get('price', '')
            price_str = re.sub(r'[\sруб]+', '', price_str)
            print(price_str)
            if '-' in price_str:
                # Если есть диапазон, разделяем его и преобразуем обе части в числа
                start, end = map(float, price_str.split('-'))
                return int(start)  # Можно добавить оба числа или минимальное
            else:
                # Для единичных чисел просто добавляем значение в список
                return int(price_str)


        # Sorting the elements by price
        sorted_elements = sorted(elements, key=get_price)[:int(message.text)]

        for element in sorted_elements:
            # Rest of your code...
            # Extracting required information
            name = element.get('name', 'No name available')
            price = element.get('price', 'No price available')
            rating = element.get('rating', 'No rating available')
            web_url = element.get('web_url', 'No web URL available')
            website = element.get('website', 'No website available')
            address = element.get('address', 'No address available')  # Извлечение адреса
            original_photo_url = element.get('photo', {}).get('images', {}).get('original', {}).get('url',
                                                                                                    'No photo URL available')
            info_text = f"Hotel Name: {name}\nPrice: {price}\nRating: {rating}\nAddress: {address}\nWeb URL: {web_url}\nWebsite: {website}"
            try:
                if original_photo_url and original_photo_url.startswith("http"):
                    await bot.send_photo(photo=original_photo_url, caption=info_text, chat_id=message.chat.id)
                else:
                    # Отправить текстовое сообщение, если URL фото недействителен
                    await bot.send_message(chat_id=message.chat.id, text=info_text)
            except Exception as e:
                # Отправить текстовое сообщение, если отправка фото не удалась
                await bot.send_message(chat_id=message.chat.id, text=info_text)
            hotel_data = {
                "web_url": web_url,
                "hotel_name": name,
                "total_price": price,
                "address": address,
                "photo_url": original_photo_url,
                "user_id": message.from_user.id,  # Ссылка на запись пользователя из предыдущего шага
                "rating": rating
            }
            save_search(user_id=message.from_user.id, search_criteria=hotel_data)

    await States.wait_command.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=States.hotel_count)
async def process_hotel_invalid(message: types.Message):
    return await message.reply("Пожалуйста, введите число.")


# END LOW COMMAND


# CUSTOM COMMAND

@dp.message_handler(commands=['custom'], state=States.wait_command)
async def custom_command(message: types.Message):
    await message.answer("Введите рейтинг отеля:", reply_markup=types.ReplyKeyboardRemove())
    await States.waiting_for_rating.set()


@dp.message_handler(state=States.waiting_for_rating)
async def rating_entered(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rating'] = message.text
    await States.waiting_for_min_price.set()
    await message.reply("Введите минимальную цену:")


@dp.message_handler(state=States.waiting_for_min_price)
async def min_price_entered(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = message.text
    await States.waiting_for_max_price.set()
    await message.reply("Введите максимальную цену:")


@dp.message_handler(state=States.waiting_for_max_price)
async def max_price_entered(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = message.text
    await message.reply('В какую страну вы хотели бы полететь?')
    await States.country_custom.set()


@dp.message_handler(state=States.country_custom)
async def process_country_custom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await States.city_custom.set()
    await message.reply("Какой город в этой стране вы хотите посетить?")


@dp.message_handler(state=States.city_custom)
async def choice_city_custom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.capitalize()
        inp = data['city'] + ' ' + data['country']
        data['city_id'] = await get_city_id(city=inp, domain=domains, locale=locales)
        if data['city_id']:
            print('City_id is okay')
    await message.answer(text='Сколько вариантов отелей вам отправить?')
    await States.hotel_count_custom.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=States.hotel_count_custom)
async def process_hotel_count_custom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        min_price = int(data['min_price'])
        max_price = int(data['max_price'])
        rating = float(data['rating'])

        hotels = await get_hotels_json(data['city_id'])
        filtered_elements = []

        for elem in hotels['results']['data']:
            price_str = re.sub(r'[^\d-]', '', elem.get('price', ''))
            prices = [int(p) for p in re.findall(r'\d+', price_str)]
            if not prices:
                continue
            min_elem_price = min(prices)
            elem_rating = float(elem.get('rating', 0))

            if (min_price <= min_elem_price <= max_price) and (elem_rating >= rating):
                filtered_elements.append(elem)

        # Сортировка отелей по минимальной цене
        sorted_elements = sorted(filtered_elements, key=lambda x: min([int(p) for p in re.findall(r'\d+', x.get('price', ''))]))

        for element in sorted_elements[:int(message.text)]:
            # Формирование и отправка сообщения для каждого отеля
            info_text = f"Hotel Name: {element.get('name', 'No name available')}\n" \
                        f"Price: {element.get('price', 'No price available')}\n" \
                        f"Rating: {element.get('rating', 'No rating available')}\n" \
                        f"Address: {element.get('address', 'No address available')}\n" \
                        f"Web URL: {element.get('web_url', 'No web URL available')}\n" \
                        f"Website: {element.get('website', 'No website available')}"
            try:
                original_photo_url = element.get('photo', {}).get('images', {}).get('original', {}).get('url', 'No photo URL available')
                if original_photo_url.startswith("http"):
                    await bot.send_photo(photo=original_photo_url, caption=info_text, chat_id=message.chat.id)
                else:
                    await bot.send_message(chat_id=message.chat.id, text=info_text)
            except Exception as e:
                await bot.send_message(chat_id=message.chat.id, text=info_text)
            hotel_data = {
                "web_url": element.get('web_url', 'No web URL available'),
                "hotel_name": element.get('name', 'No name available'),
                "total_price": element.get('price', 'No price available'),
                "address": element.get('address', 'No address available'),
                "photo_url": original_photo_url,
                "user_id": message.from_user.id,  # Ссылка на запись пользователя из предыдущего шага
                "rating": element.get('rating', 'No rating available')
            }
            save_search(user_id=message.from_user.id, search_criteria=hotel_data)

    await States.wait_command.set()



# END CUSTOM COMMAND

#HIGH COMMAND

@dp.message_handler(commands=['high'], state=States.wait_command)
async def cmd_high(message: types.Message):
    await States.country_high.set()
    await message.reply("В какую страну вы хотели бы полететь?")


@dp.message_handler(state=States.country_high)
async def process_country_high(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await States.city_high.set()
    await message.reply("Какой город в этой стране вы хотите посетить?")


@dp.message_handler(state=States.city_high)
async def choice_city_high(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.capitalize()
        inp = data['city'] + ' ' + data['country']
        data['city_id'] = await get_city_id(city=inp, domain=domains, locale=locales)
        if data['city_id']:
            await message.answer(text='City_id is okay')

    await message.answer(text='Сколько вариантов отелей вам отправить?')
    await States.process_hotel_count_high.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=States.process_hotel_count_high)
async def process_hotel_count_high(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hotel_count'] = int(message.text)
        hotels = await get_hotels_json(data['city_id'])
        elements = []
        for elem in hotels['results']['data']:
            if elem.get('price', '') != '':
                elements.append(elem)

        # Проверяем, что все элементы в filtered_data имеют 'price'
        all_have_price = all('price' in elem and elem['price'] != '' for elem in elements)

        if all_have_price:
            print("Все элементы в filtered_data имеют 'price'")
            hotels['results']['data'] = elements
        else:
            print("Некоторые элементы в filtered_data не имеют 'price'")

        # Function to extract numerical price from the price string
        def get_price(element):
            print(element.get('price', '').split())
            price_str = element.get('price', '')
            price_str = re.sub(r'[\sруб]+', '', price_str)
            print(price_str)
            if '-' in price_str:
                # Если есть диапазон, разделяем его и преобразуем обе части в числа
                start, end = map(float, price_str.split('-'))
                return int(start)  # Можно добавить оба числа или минимальное
            else:
                # Для единичных чисел просто добавляем значение в список
                return int(price_str)

        # Sorting the elements by price
        sorted_elements = sorted(elements, key=get_price, reverse=True)[:int(message.text)]

        for element in sorted_elements:
            # Rest of your code...
            # Extracting required information
            name = element.get('name', 'No name available')
            price = element.get('price', 'No price available')
            rating = element.get('rating', 'No rating available')
            web_url = element.get('web_url', 'No web URL available')
            website = element.get('website', 'No website available')
            address = element.get('address', 'No address available')  # Извлечение адреса
            original_photo_url = element.get('photo', {}).get('images', {}).get('original', {}).get('url',
                                                                                                    'No photo URL available')
            info_text = f"Hotel Name: {name}\nPrice: {price}\nRating: {rating}\nAddress: {address}\nWeb URL: {web_url}\nWebsite: {website}"
            try:
                if original_photo_url and original_photo_url.startswith("http"):
                    await bot.send_photo(photo=original_photo_url, caption=info_text, chat_id=message.chat.id)
                else:
                    # Отправить текстовое сообщение, если URL фото недействителен
                    await bot.send_message(chat_id=message.chat.id, text=info_text,)
            except Exception as e:
                # Отправить текстовое сообщение, если отправка фото не удалась
                await bot.send_message(chat_id=message.chat.id, text=info_text, reply_markup=get_kb_commands(commands))
            hotel_data = {
                "web_url": web_url,
                "hotel_name": name,
                "total_price": price,
                "address": address,
                "photo_url": original_photo_url,
                "user_id": message.from_user.id,  # Ссылка на запись пользователя из предыдущего шага
                "rating": rating
            }
            save_search(user_id=message.from_user.id, search_criteria=hotel_data)
    await States.wait_command.set()


#END HIGH COMMAND


@dp.message_handler(state=States.wait_command, commands=['history'])
async def send_search_history(message: types.Message):
    user_id = str(message.from_user.id)  # Получение Telegram ID пользователя
    history = get_user_search_history(user_id)  # Запрос истории поиска из базы данных
    formatted_history = format_search_history(history)  # Форматирование истории для вывода
    await message.answer(formatted_history)  # Отправка истории пользователю
