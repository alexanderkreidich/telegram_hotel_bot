from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

commands = ['/help', '/low', '/high', '/custom', '/history']
domains = ["US","PT","SE","SG","TH","TR","TW","US","VN","XE","ZA"]
locales = ['en_US']


def get_ikb_commands(data: list) -> InlineKeyboardMarkup:
    ikb_commands = InlineKeyboardMarkup(row_width=2)
    [ikb_commands.add(InlineKeyboardButton(cmd)) for cmd in data]
    return ikb_commands


