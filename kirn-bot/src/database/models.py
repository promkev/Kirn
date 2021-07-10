import peewee
import datetime
import os

db = peewee.SqliteDatabase(os.path.join(
    os.path.dirname(__file__), '..', 'data', 'database.db'))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Guild(BaseModel):
    guild_id = peewee.TextField(unique=True)
    prefix = peewee.TextField()

    # class Meta:
    #     primary_key = peewee.ke


class Course(BaseModel):
    guild_id = peewee.TextField()
    course_name = peewee.TextField()
    category = peewee.TextField()

    class Meta:
        primary_key = peewee.CompositeKey('guild_id', 'course_name')


db.connect()
db.create_tables([Guild, Course])
