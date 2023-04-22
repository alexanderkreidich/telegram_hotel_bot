from database.core import crud
from aiogram import Bot, Dispatcher, executor
from settings import SiteSettings

site = SiteSettings()

db_write = crud.create()
db_read = crud.retrieve()

bot = Bot(site.token.get_secret_value())
dp = Dispatcher(bot)

from tg_API.utils.handlers import start_command, help_command, high_command, custom_command, history_command

handlers = [start_command, help_command, high_command, custom_command, history_command]
for handler in handlers:
    dp.register_message_handler(handler)

if __name__ == '__main__':
    executor.start_polling(dp)
