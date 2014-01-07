
import datetime
import feedparser
import sys

from flask import current_app
from .models import *

from flask.ext.script import Manager
manager = Manager(usage="Perform database operations")

@manager.command
def drop():
    """Drop all tables."""
    Date.drop_table(fail_silently=True)
    Feed.drop_table(fail_silently=True)
    Entry.drop_table(fail_silently=True)
    print('All tables dropped.')

@manager.command
def create():
    """Create all tables."""
    Date.create_table(fail_silently=True)
    Feed.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
    print('All tables created.')

@manager.command
def list():
    """Show a list of all stored feeds."""
    for feed in Feed.select():#.order_by(Feed.title.desc()):
        print('#%i. %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def add(link, title=''):
    """Add a new feed with a URL and optionally a title."""
    if not link.startswith('http://'):
        link = 'http://%s' % link
    try:
        Feed.create(title=title or link, link=link)
    except Exception as e:
        print('Error while adding new feed: %s' % e)
        sys.exit(1)
    print('New feed has been stored.')

@manager.command
def remove(idno):
    """Remove a feed, using it's ID number."""
    try:
        feed = Feed.get(Feed.id == idno)
    except Exception as e:
        print('Error while removing feed: %s' % e)
        sys.exit(1)
    print('Now removing feed #%i . %s (%s)' % (feed.id, feed.title, feed.link))
    feed.delete_instance()

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
        print('Updating %s with %i new items.' % (feed.title, stored))
