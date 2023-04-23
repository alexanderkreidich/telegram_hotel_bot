from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import SiteSettings


storage = MemoryStorage()

site = SiteSettings()
bot = Bot(site.token.get_secret_value())
dp = Dispatcher(bot, storage=storage)