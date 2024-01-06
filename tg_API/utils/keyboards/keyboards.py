from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

commands = ['/help', '/low', '/high', '/custom', '/history', ]
domains = ["AE"]
locales = ['en_GB']
country = []


def get_kb_commands(data: list) -> ReplyKeyboardMarkup:
    kb_commands = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    [kb_commands.add(cmd) for cmd in data]
    return kb_commands
