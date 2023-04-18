#TODO FIX AttributeError: module 'aiogram.dispatcher' has no attribute 'message_handler'

from aiogram import types
from aiogram import dispatcher as dp
import keyboards


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
    await message.answer(text='Выберите команду', reply_markup=keyboards.ikb_commands)


@dp.message_handler(commands=['help'])
async def settings_command(message: types.Message):
    await message.answer(text=help_text)
