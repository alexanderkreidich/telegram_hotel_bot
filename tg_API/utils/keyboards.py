from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

commands = ['/help', '/low', '/high', '/custom', '/history']
domains = [AE,AR,AS,AT,AU,BE,BR,CA,CH,CL,CN,CO,DE,DK,ES,FI,FR,GB,GR,HK,HU,ID,IE,IN,IS,IT,JP,KR,MX,MY,NL,NO,NZ,PE,PH,"PT","SE","SG","TH","TR","TW","US","VN","XE","ZA"]
locales = ['en_US']


def get_ikb_commands(data: list) -> InlineKeyboardMarkup:
    ikb_commands = InlineKeyboardMarkup(row_width=2)
    [ikb_commands.add(InlineKeyboardButton(cmd)) for cmd in data]
    return ikb_commands


