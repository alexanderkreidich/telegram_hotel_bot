# TODO FIX AttributeError: module 'aiogram.dispatcher' has no attribute 'message_handler'
from aiogram import types
from aiogram.dispatcher import FSMContext
from tg_API.utils.keyboards.keyboards import get_kb_commands, domains, commands, locales
from site_API.utils.parse_responses.parse_hotel_resp import hotel_info, get_city_id, get_hotels
from tg_API.utils.states.state import States
from load_bot import dp, bot

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


@dp.message_handler(state=States.get_domain)
async def choice_domain(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['domain'] = message.text
    await message.answer(text='Дальше выберите название вашего региона:', reply_markup=get_kb_commands(locales))
    await States.get_locale.set()


@dp.message_handler(lambda message: message not in domains, state=States.get_domain)
async def choice_domain_incorrectly(message: types.Message):
    return await message.answer(text='не знаю такого домена. Введите еще раз:', reply_markup=get_kb_commands(domains))


@dp.message_handler(state=States.get_locale)
async def choice_locale(message: types.Message, state: FSMContext):
    await state.update_data(get_locale=message.text)
    async with state.proxy() as data:
        data['locale'] = message.text
    await message.answer(text='Пожалуйста, укажите город для поиска')
    await States.select_cities.set()


@dp.message_handler(lambda message: message not in locales, state=States.get_locale)
async def choice_locale_incorrectly(message: types.Message):
    await message.answer(text='не знаю такого региона. Введите еще раз:', reply_markup=get_kb_commands(locales))


@dp.message_handler(state=States.wait_command, commands=['custom'])
async def custom_command(message: types.Message):
    await message.answer(text='Выберите название вашего домена:', reply_markup=get_kb_commands(domains))
    await States.get_domain.set()


@dp.message_handler(state=States.select_cities)
async def choice_cities(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        cities: dict = await get_city_id(message.text, locale=data['locale'], domain=data['domain'])
        cities_names = [key for key in cities.keys()]
        await message.answer(text='Выберите город', reply_markup=get_kb_commands(cities_names))
        data['cities'] = cities
        await States.select_city.set()


@dp.message_handler(state=States.select_city)
async def choice_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['cities'][message.text] is not None:
            data['city_id'] = data['cities'][message.text]
    await message.answer(text='Отлично! Теперь введите дату заезда в таком формате yyyy-mm-dd')
    await States.select_date_in.set()


@dp.message_handler(lambda msg: len(msg.text.split('-')) == 3, state=States.select_date_in)
async def choice_date_in(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_in'] = message.text
    await message.answer(text='Теперь введите дату выезда по этому формату')
    await States.select_date_out.set()


@dp.message_handler(lambda msg: len(msg.text.split('-')) == 3, state=States.select_date_out)
async def choice_date_out(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_out'] = message.text
    await message.answer('Выберите скольки звездочные отели выбирать?')
    await States.select_stars.set()


@dp.message_handler(state=States.select_stars)
async def choice_stars(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stars'] = message.text
        print(data)
    await message.answer('Отлично! вы закончили выбор параметров!')
    await message.answer(text='Выберите команду', reply_markup=get_kb_commands(commands))
    await States.wait_command.set()


@dp.message_handler(state=States.wait_command, commands=['high'])
async def high_command(message: types.Message):
    await message.answer(text='Сколько вывести отелей?')
    await States.select_Pages.set()


@dp.message_handler(lambda msg: msg.text.isdigit(), state=States.select_Pages)
async def select_pages(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        hotels = await get_hotels(domain=data['domain'], sort_order='PRICE_LOW_TO_HIGH', locale=data['locale'],
                                  region_id=data['city_id'], checkin_date=data['date_in'],
                                  checkout_date=data['date_out'], adults_number='1')
        for page in range(int(message.text)):
            hotel_id = hotels['properties'][page]['id']
            print(hotel_id)

            hotel: dict = await hotel_info(domain=data['domain'], locale=data['locale'], hotel_id=hotel_id)
            text = f'Отель: {hotel["name"]}\nРейтинг: {hotel["stars"]}\nЕхать от Аэропорта {hotel["title"]}: {hotel["time"]} минут'
            await bot.send_photo(photo=hotel['Photo_1'], caption=text, chat_id=message.chat.id)
            States.wait_command.set()


@dp.message_handler(state=States.wait_command, commands=['history'])
async def history_command(message: types.Message):
    history = ''  # здесь должен быть вывод истории запросов пользователей
    await message.answer(text=f'Ваша история запросов:\n{history}')
