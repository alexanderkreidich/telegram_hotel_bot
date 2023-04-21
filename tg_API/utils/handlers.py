# TODO FIX AttributeError: module 'aiogram.dispatcher' has no attribute 'message_handler'
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from magic_filter import F

from main import dp
from keyboards import get_ikb_locale, get_ikb_commands, get_ikb_domains, domains, commands, locales
from site_API.utils.parse_responses.parse_hotel_resp import get_hotel_info_json


class Region_Info(StatesGroup):
    get_locale = State()
    get_domain = State()
    get_city = State()


help_text = """
Команды:
● /help — помощь по командам бота;
● /low — вывод минимальных показателей (с изображением товара/услуги/и так
далее);
● /high — вывод максимальных (с изображением товара/услуги/и так далее);
● /custom — вывод показателей пользовательского диапазона (с изображением
товара/услуги/и так далее);
/history — вывод истории запросов пользователей."""


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Добро пожаловать в KickSwitchHotels! Это телеграмм-бот,'
                              ' для поиска отелей по оптимальной цене!'
                              ' Надеюсь этот бот будет для вас полезным!')
    await message.answer(text='Выберите команду', reply_markup=get_ikb_commands(commands))


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=help_text)


@dp.message_handler(commands=['low'])
async def low_command(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите название вашего домена:', reply_markup=get_ikb_domains(domains))
    await state.set_state(Region_Info.get_domain)


@dp.message_handler(Region_Info.get_domain,
                    F.text.in_(domains))
async def choose_domain(message: types.Message, state: FSMContext):
    await state.update_data(get_domain=message.text.lower())
    await message.answer(text='Дальше выберите название вашего региона:', reply_markup=get_ikb_locale(locales))
    await state.set_state(Region_Info.get_locale)


@dp.message_handler(Region_Info.get_domain)
async def choose_domain_incorrectly(message: types.Message):
    await message.answer(text='не знаю такого домена. Введите еще раз:', reply_markup=get_ikb_domains(domains))


@dp.message_handler(Region_Info.get_locale,
                    F.text.in_(locales))
async def choose_locale(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f'Вы выбрали domain:{user_data["get_domain"]}\nlocale:{message.text.lower()}')
    await state.clear()


@dp.message_handler(Region_Info.get_locale)
async def choose_domain_incorrectly(message: types.Message):
    await message.answer(text='не знаю такого региона. Введите еще раз:', reply_markup=get_ikb_domains(locales))

@dp.message_handler(Region_Info.get_domain,
                    F.text.in_(domains))
async def choose_city(message: types.Message, state: FSMContext):
    await message.answer(text='Введите город название города:')
    await state.set_state(Region_Info.get_city)



