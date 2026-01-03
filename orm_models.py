import os
from peewee import SqliteDatabase, Model, CharField, IntegerField, TextField

db_path = os.getenv("MOVIES_EXTENDED_DB", "movies-extended.db")
db = SqliteDatabase(db_path)

class BaseModel(Model):

    class Meta:
        database = db

class Movie(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField()
    director = CharField()
    year = IntegerField()
    description = TextField()

class Actor(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    surname = CharField()
