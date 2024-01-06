#TODO Сделать модели юзера и сделать историю поиска и базу данных, которая будет содержать айди юзера и всю его историю поиска
# чтобы при перезагрузке оставалась история пользователя определенного

from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('tg_bot.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class History(ModelBase):
    message = pw.TextField()

