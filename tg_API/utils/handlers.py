# TODO FIX AttributeError: module 'aiogram.dispatcher' has no attribute 'message_handler'
from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from magic_filter import F
from settings import SiteSettings
from keyboards import get_ikb_commands, domains, commands, locales
from site_API.utils.parse_responses.parse_hotel_resp import get_hotel_info_json


class Region_Info(StatesGroup):
    get_locale = State()
    get_domain = State()
    get_city = State()


site = SiteSettings()
bot = Bot(site.token.get_secret_value())
dp = Dispatcher(bot)


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


@dp.message_handler(commands=['high'])
async def high_command(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите название вашего домена:', reply_markup=get_ikb_commands(domains))
    await state.set_state(Region_Info.get_domain.state)


@dp.message_handler(commands=['custom'])
async def custom_command(message: types.Message, state: FSMContext):
    await message.answer(text='Пожалуйста, укажите параметры вашего запроса (ценовой диапазон, кол-во звезд и т.д.)')
    await state.set_state(Region_Info.get_city.state)


@dp.message_handler(commands=['history'])
async def history_command(message: types.Message):
    history = ''  # здесь должен быть вывод истории запросов пользователей, но я не знаю как это реализовать
    await message.answer(text=f'Ваша история запросов:\n{history}')





