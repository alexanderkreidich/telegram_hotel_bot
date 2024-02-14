# TODO  заменить домейн и локал на страны беларусь, грузия, казахстан, абхазия
# Изменить кнопку хай чтобы город выбирался уже после ее нажатия
# сделать кнопку low
# добаввить адрес отеля и ссылку на карты, чтобы можно было сразу построить маршрут 
import aiogram

from tg_API.utils.states.state import States
from load_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types, utils
from site_API.utils.parse_responses.parse_hotel_resp import get_city_id, get_hotels_json
from tg_API.utils.keyboards.keyboards import get_kb_commands, domains, commands, locales
import re

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
    current_state = await state.get_state()
    if current_state is None:
        return
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
        data['city'] = message.text
        inp = data['city'] + ' ' + data['country']
        data['city_id'] = await get_city_id(city=inp, domain=domains, locale=locales)
        if data['city_id']:
            await message.answer(text='City_id is okay')

    await message.answer(text='Сколько вариантов отелей вам отправить?')
    await States.hotel_count_custom.set()

@dp.message_handler(state=States.city)
async def choice_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
        inp = data['city'] + ' ' + data['country']
        data['city_id'] = await get_city_id(city=inp, domain=domains, locale=locales)
        if data['city_id']:
            await message.answer(text='City_id is okay')

    await message.answer(text='Сколько вариантов отелей вам отправить?')
    await States.hotel_count_custom.set()



@dp.message_handler(lambda message: message.text.isdigit(), state=States.hotel_count)
async def process_hotel_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hotel_count'] = int(message.text)
        hotels = await get_hotels_json(data['city_id'])
        elements = []
        for elem in hotels['results']['data']:
            if elem.get('price', '') != '' and elem.get('price_level', '') != '':
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

    # all the shit goes

    await States.country.set()


# END CUSTOM COMMAND

@dp.message_handler(state=States.wait_command, commands=['history'])
async def history_command(message: types.Message):
    history = ''  # здесь должен быть вывод истории запросов пользователей
    await message.answer(text=f'Ваша история запросов:\n{history}')
