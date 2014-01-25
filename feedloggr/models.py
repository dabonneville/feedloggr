
from peewee import DateField, CharField, ForeignKeyField
from flask_peewee.admin import ModelAdmin

from peewee import Proxy, Model
# Use a proxy so we can define the models now and init the database at
# a later time.
db_proxy = Proxy()

######################################################################

class FeedsAdmin(ModelAdmin):
    """Show pretty admin interface for feeds."""
    columns = ('title', 'link')

######################################################################

class BaseModel(Model):
    class Meta:
        database = db_proxy

class Dates(BaseModel):
    """Stores dates as datetime.date objects."""
    date = DateField(null=False, unique=True)

class Feeds(BaseModel):
    """Stores RSS/Atom feeds with a title and link."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)

class Entries(BaseModel):
    """Stores news items with a title, link, date and feed."""
    title = CharField(null=False)
    link = CharField(null=False, unique=True)
    date = ForeignKeyField(Dates)
    feed = ForeignKeyField(Feeds)

