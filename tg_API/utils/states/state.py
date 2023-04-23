from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    get_domain = State()
    get_locale = State()
    select_cities = State()
    select_city = State()
    select_date_in = State()
    select_date_out = State()
    select_stars = State()
    select_Pages = State()
    print_hotels = State()
    wait_command = State()





