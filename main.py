from aiogram import executor
import tg_API.utils.handlers.handlers
from load_bot import *


async def on_startup(_):
    print('Я запустился')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
