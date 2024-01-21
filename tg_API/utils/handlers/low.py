from tg_API.utils.states.state import States
from load_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from site_API.utils.parse_responses.parse_hotel_resp import get_city_id
from tg_API.utils.keyboards.keyboards import get_kb_commands, domains, commands, locales

@dp.message_handler(commands=['low'])
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
        data['city_id'] = get_city_id(city=data['city'] + ' ' + data['country'], domain=domains, locale=locales)
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
    await message.answer('Сколько вариантов отелей вам отправить?')
    await States.hotel_count.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=States.hotel_count)
async def process_hotel_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hotel_count'] = int(message.text)
        hotels = get_ho
        for page in range(int(message.text)):


    await States.wait_command.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=States.hotel_count)
async def process_hotel_invalid(message: types.Message):
    return await message.reply("Пожалуйста, введите число.")

