import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('events.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

class Event(Model):
    title = CharField() 
    venueNa = CharField() 
    city = CharField()
    # time = CharField()
    # location = CharField()
    # tickets = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta: 
        database = DATABASE 

def initialize(): 
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True) 
    print("TABLES Created")
    DATABASE.close()


    