from database.core import crud
from aiogram import Bot, Dispatcher, executor
from settings import SiteSettings
site = SiteSettings()

db_write = crud.create()
db_read = crud.retrieve()

bot = Bot(site.token.get_secret_value())
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp)


