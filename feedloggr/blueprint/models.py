
from peewee import DateField, CharField, ForeignKeyField
from flask_peewee.admin import ModelAdmin

from app import db

######################################################################

class FeedsAdmin(ModelAdmin):
    """Show pretty admin interface for feeds."""
    columns = ('title', 'link')

class Dates(db.Model):
    """Stores dates as datetime.date objects."""
    date = DateField(null=False, unique=True)

class Feeds(db.Model):
    """Stores RSS/Atom feeds with a title and link."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)

class Entries(db.Model):
    """Stores news items with a title, link, date and feed."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)
    date = ForeignKeyField(Dates)
    feed = ForeignKeyField(Feeds)

