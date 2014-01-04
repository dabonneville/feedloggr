
from peewee import *

from app import db

######################################################################

class BaseModel(Model):
    class Meta:
        database = db

class Date(BaseModel):
    date = DateField(null=False, unique=True)

class Feed(BaseModel):
    title = CharField(null=False)
    link = CharField(null=False, unique=True)

class Entry(BaseModel):
    title = CharField(null=False)
    link = CharField(null=False, unique=True)
    date = ForeignKeyField(Date)
    feed = ForeignKeyField(Feed)

