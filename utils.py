
import datetime
import feedparser

from flask import current_app
from .models import *

from flask.ext.script import Manager
manager = Manager(usage="Perform database operations")

@manager.command
def reset():
    """Reset all tables."""
    Date.drop_table(fail_silently=True)
    Feed.drop_table(fail_silently=True)
    Entry.drop_table(fail_silently=True)
    Date.create_table(fail_silently=True)
    Feed.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
    print('All tables cleared.')

@manager.command
def update():
    """Update all feeds stored in the database."""
    date = Date.get_or_create(date=datetime.date.today()) # TODO
    for feed in Feed.select():
        data = feedparser.parse(feed.link)
        items = min(current_app.config['FEEDLOGGR_MAX_ITEMS'], len(data.entries))

        stored = 0
        with db.transaction():
            for i in xrange(items):
                item = data.entries[i]
                try:
                    entry = Entry.get(link=item['link'])
                except DoesNotExist:
                    entry = Entry.create(
                        title = item['title'] or item['link'],
                        link = item['link'],
                        date = date,
                        feed = feed,
                    )
                    stored += 1
        print('Updating %s with %i new items, out of %i (%i%%).' % (feed.title, stored, items, (float(stored)/items) * 100))
