from peewee import *
import datetime
from flask_login import UserMixin 
import random


DATABASE = SqliteDatabase('events.sqlite')

class User(UserMixin, Model):
    username = CharField()
    email = CharField()
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE


class Event(Model):
    title = CharField() 
    venueName = CharField() 
    city = CharField()
    # time = CharField()
    # location = CharField()
    # tickets = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
    

class UserEvent(Model):
    user = ForeignKeyField(User)
    event = CharField()

    class Meta:
        database = DATABASE

def initialize(): 
    DATABASE.connect()
    DATABASE.create_tables([User, Event, UserEvent], safe=True) 
    print('TABLES Created')
    DATABASE.close()

