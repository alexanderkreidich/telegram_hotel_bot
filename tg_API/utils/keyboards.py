from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_commands = InlineKeyboardMarkup(row_width=2)
commands = ['/help', '/low', '/high', '/custom', '/history']
for cmd in commands:
    ikb_commands.add(InlineKeyboardButton(cmd))

