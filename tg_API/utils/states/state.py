from aiogram.dispatcher.filters.state import StatesGroup, State


class Region_Info(StatesGroup):
    get_locale = State()
    get_domain = State()


class SelectCity(StatesGroup):
    select_city = State()



