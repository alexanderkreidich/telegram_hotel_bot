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
    hotels_found = pw.TextField()


class Hotel_Data(ModelBase):
    user_id = pw.ForeignKeyField(User)
    property_id  = pw.TextField(primary_key=True)
    hotel_name = pw.TextField(unique=True)
    distance_from_center = pw.TextField()
    nightly_price = pw.TextField()
    total_price = pw.TextField()
    address = pw.TextField()
    photo_url = pw.TextField(unique=True)
    reviews_score = pw.IntegerField()
    reviews_total = pw.IntegerField()

class Hotel_Photos(ModelBase):
    hotel_id = pw.ForeignKeyField(Hotel_Data)
    photo_links = pw.TextField(unique=True)


db.connect()
db.create_tables([JsonData])
db.close()

