
import datetime

from .models import *

######################################################################

def create_tables(fail_silently=True):
    Date.create_table(fail_silently=fail_silently)
    Feed.create_table(fail_silently=fail_silently)
    Entry.create_table(fail_silently=fail_silently)

def drop_tables(fail_silently=True):
    Date.drop_table(fail_silently=fail_silently)
    Feed.drop_table(fail_silently=fail_silently)
    Entry.drop_table(fail_silently=fail_silently)

def get_news(current_date = datetime.date.today()):
    news = []
    date = Date.get_or_create(date = current_date) # TODO
    if not date:
        return news
    for feed in Feed.select().order_by(Feed.title.desc()):
        items = Entry.select().where(
            Entry.feed == feed,
            Entry.date == date
        )
        if items.count() > 0:
            news.append((feed, items))
    return news

def update_feeds():
    import feedparser
    from flask import current_app
    from peewee import IntegrityError as pie
    date = Date.get_or_create(date=datetime.date.today()) # TODO
    new_items = 0
    for feed in Feed.select():
        data = feedparser.parse(feed.link)
        max_items = current_app.config['FEEDLOGGR_MAX_ITEMS'] or 25
        items = min(max_items, len(data.entries))
        with db.transaction(): # avoids comitting after each new item
            for i in xrange(items):
                item = data.entries[i]
                try:
                    entry = Entry.create(
                        title = item['title'] or item['link'],
                        link = item['link'],
                        date = date,
                        feed = feed,
                    )
                except pie:
                    # TODO: peewee is complaining via a log handler
                    pass
                else:
                    new_items += 1
    return new_items

######################################################################

from flask.ext.script import Manager
manager = Manager(usage="Perform database operations")

@manager.command
def reset():
    """Reset all tables, by dropping and recreating them."""
    drop_tables()
    create_tables()
    print('All tables reset.')

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
    else:
        print('New feed has been stored.')

@manager.command
def remove(idno):
    """Remove a feed, using it's ID number."""
    try:
        feed = Feed.get(Feed.id == idno)
        feed.delete_instance()
    except Exception as e:
        print('Error while removing feed: %s' % e)
    else:
        print('Removed feed #%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def update():
    """Update all feeds stored in the database."""
    new_items = update_feeds()
    print('Database was updated with %i new items.' % new_items)

