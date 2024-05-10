import logging
from peewee import *
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('tg_bot.db')

class ModelBase(Model):
    created_at = DateField(default=datetime.now)
    class Meta:
        database = db

class User(ModelBase):
    user_id = IntegerField(unique=True)

class Hotel_Data(ModelBase):
    user_id = ForeignKeyField(User, backref='hotels')
    hotel_name = TextField()
    total_price = TextField()
    address = TextField()
    photo_url = TextField()
    rating = TextField()
    web_url = TextField()
    website = TextField()

db.connect()
db.create_tables([User, Hotel_Data])

def ensure_user_exists(user_id):
    user, created = User.get_or_create(user_id=user_id)
    return user

def save_search(user_id, hotel_info):
    user = ensure_user_exists(user_id)

    try:
        hotel = Hotel_Data.create(
            user_id=user.id,
            hotel_name=hotel_info['hotel_name'],
            total_price=hotel_info['total_price'],
            address=hotel_info['address'],
            photo_url=hotel_info['photo_url'],
            rating=hotel_info['rating'],
            web_url=hotel_info['web_url'],
            website=hotel_info['website']
        )
        logger.info("Успешно сохранены данные")
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных об отеле: {e}")
    # Проверяем количество записей для пользователя и удаляем старые, если их больше 10
    try:
        # Получаем список всех записей поиска для пользователя, отсортированный по дате создания (от новых к старым)
        hotel_records = Hotel_Data.select().where(Hotel_Data.user_id == user.id).order_by(Hotel_Data.created_at.desc())

        # Если записей больше 10, удаляем самые старые
        if hotel_records.count() > 10:
            # Определяем ID записей, которые нужно удалить (все кроме последних 10)
            ids_to_delete = [hotel.id for hotel in hotel_records][10:]

            # Удаление записей
            Hotel_Data.delete().where(Hotel_Data.id.in_(ids_to_delete)).execute()
            logger.info("Старые записи поиска удалены")
    except Exception as e:
        logger.error(f"Ошибка при удалении старых записей поиска: {e}")


def get_hotels_for_user(user_id):
    try:
        hotels = Hotel_Data.select().join(User).where(User.user_id == user_id)
        return hotels
    except DoesNotExist:
        return []

