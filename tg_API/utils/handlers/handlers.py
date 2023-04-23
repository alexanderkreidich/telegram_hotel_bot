# TODO FIX AttributeError: module 'aiogram.dispatcher' has no attribute 'message_handler'
from aiogram import types
from aiogram.dispatcher import FSMContext
from tg_API.utils.keyboards.keyboards import get_ikb_commands, domains, commands, locales
from site_API.utils.parse_responses.parse_hotel_resp import get_hotel_info_json
from tg_API.utils.states.state import SelectCity, Region_Info
from load_bot import dp


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
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в KickSwitchHotels! Это телеграмм-бот,'
                              ' для поиска отелей по оптимальной цене!'
                              ' Надеюсь этот бот будет для вас полезным!')
    await message.answer(text='Выберите команду', reply_markup=get_ikb_commands(commands))


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=help_text)


@dp.message_handler(commands=['settings'])
async def high_command(message: types.Message):
    await message.answer(text='Выберите название вашего домена:', reply_markup=get_ikb_commands(domains))
    await Region_Info.get_domain.set()


@dp.message_handler(state=Region_Info.get_domain)
async def choose_domain(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['domain'] = message.text
    await message.answer(text='Дальше выберите название вашего региона:', reply_markup=get_ikb_commands(locales))
    await Region_Info.next()


@dp.message_handler(lambda message: message not in domains, state=Region_Info.get_domain)
async def choose_domain_incorrectly(message: types.Message):
    return await message.answer(text='не знаю такого домена. Введите еще раз:', reply_markup=get_ikb_commands(domains))


@dp.message_handler(lambda message: message in locales, state=Region_Info.get_locale)
async def choose_locale(message: types.Message, state: FSMContext):
    await Region_Info.next()
    await state.update_data(get_locale=message.text)
    async with state.proxy() as data:
        data['locale'] = message.text
        await message.answer(f'Вы выбрали domain:{data["domain"]}\nlocale:{data["locale"]}')

    await state.finish()


@dp.message_handler(lambda message: message not in locales, state=Region_Info.get_locale)
async def choose_locale_incorrectly(message: types.Message):
    return await message.answer(text='не знаю такого региона. Введите еще раз:', reply_markup=get_ikb_commands(locales))


@dp.message_handler(commands=['custom'])
async def custom_command(message: types.Message):
    await message.answer(text='Пожалуйста, укажите параметры вашего запроса (ценовой диапазон, кол-во звезд и т.д.)')
    await SelectCity.select_city.set()


@dp.message_handler(commands=['history'])
async def history_command(message: types.Message):
    history = ''  # здесь должен быть вывод истории запросов пользователей
    await message.answer(text=f'Ваша история запросов:\n{history}')





