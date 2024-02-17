from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    curr_state = State()
    waiting_for_rating = State()
    waiting_for_min_price = State()
    waiting_for_max_price = State()
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
    hotel_count_custom = State()
    city_custom = State()
    country_custom = State()
    process_hotel_count_high = State()
    city_high = State()
    country_high = State()




