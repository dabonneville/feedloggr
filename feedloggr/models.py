
from peewee import DateField, CharField, ForeignKeyField

from app import db

######################################################################

class Date(db.Model):
    """Stores dates as datetime.date objects."""
    date = DateField(null=False, unique=True)

class Feed(db.Model):
    """Stores RSS/Atom feeds with a title and link."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)

class Entry(db.Model):
    """Stores news items with a title, link, date and feed."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)
    date = ForeignKeyField(Date)
    feed = ForeignKeyField(Feed)

