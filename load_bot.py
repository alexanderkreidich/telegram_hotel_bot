from aiogram import Dispatcher, Bot

from settings import SiteSettings

site = SiteSettings()
bot = Bot(site.token.get_secret_value())
dp = Dispatcher(bot)