from peewee import *
import datetime
from flask_login import UserMixin 


DATABASE = SqliteDatabase('events.sqlite')

class User(UserMixin, Model):
    username = CharField()
    email = CharField()
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta: 
        database  = DATABASE

class Event(Model):
    sport = CharField() 
    teams = CharField() 
    date = CharField()
    time = CharField()
    location = CharField()
    tickets = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta: 
        database = DATABASE


def initialize(): 
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True) 
    print('TABLES Created')
    DATABASE.close()

