from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    select_date_in = State()
    select_date_out = State()
    select_stars = State()
    select_Pages = State()
    print_hotels = State()
    wait_command = State()
    country = State()  # Название страны
    city = State()     # Название города
    hotel_count = State()  # Количество отелей
    city_id = State()




