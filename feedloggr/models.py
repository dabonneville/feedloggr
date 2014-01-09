
from peewee import *

from app import db

######################################################################

class Date(db.Model):
    date = DateField(null=False, unique=True)

class Feed(db.Model):
    title = CharField(null=False)
    link = CharField(null=False, unique=True)

class Entry(db.Model):
    title = CharField(null=False)
    link = CharField(null=False, unique=True)
    date = ForeignKeyField(Date)
    feed = ForeignKeyField(Feed)

