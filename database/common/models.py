#TODO Сделать модели юзера и сделать историю поиска и базу данных, которая будет содержать айди юзера и всю его историю поиска
# чтобы при перезагрузке оставалась история пользователя определенного

from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('tg_bot.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db

class User(ModelBase):
    user_id = pw.IntegerField()
    hotels_found = pw.IntegerField()


class Hotel_Data(ModelBase):
    user_id = pw.ForeignKeyField(User)
    hotel_name = pw.TextField(unique=True)
    total_price = pw.TextField()
    address = pw.TextField()
    photo_url = pw.TextField(unique=True)
    rating = pw.IntegerField()
    web_url = pw.TextField()
    website = pw.TextField()


def save_search(user_id, search_criteria):
    # Сохранение нового поиска
    User.create(user_id=user_id, hotels_found=search_criteria)

    # Получение всех поисковых запросов пользователя, отсортированных по дате (от самых новых к самым старым)
    search_history = User.select().where(User.user_id == user_id).order_by(User.created_at.desc())

    # Подсчет количества записей
    count = search_history.count()

    # Если записей больше 10, удаляем самые старые
    if count > 10:
        # Определение ID записей, которые нужно удалить
        ids_to_delete = [search.id for search in search_history[10:]]

        # Удаление записей
        User.delete().where(User.id.in_(ids_to_delete)).execute()

def get_user_search_history(user_id):
    try:
        # Предполагаем, что user_id - это поле в модели User, которое хранит идентификатор пользователя
        search_history = (User
                          .select()
                          .where(User.user_id == user_id)
                          .order_by(User.created_at.desc()))
        return search_history
    except User.DoesNotExist:
        return None


def format_search_history(history):
    if not history:
        return "История поиска пуста."

    history_messages = []
    for record in history:
        message = f"Запрос: {record.hotels_found}, Дата: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        history_messages.append(message)

    return "\n".join(history_messages)
