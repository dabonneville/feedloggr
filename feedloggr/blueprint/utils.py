
import datetime

from peewee import IntegrityError as pie
from peewee import DoesNotExist as pdne

from .models import Date, Feed, Entry, db

######################################################################

def create_tables(fail_silently=True):
    """Create database tables used by feedloggr."""
    Date.create_table(fail_silently=fail_silently)
    Feed.create_table(fail_silently=fail_silently)
    Entry.create_table(fail_silently=fail_silently)

def drop_tables(fail_silently=True):
    """Drop database tables used by feedloggr."""
    Date.drop_table(fail_silently=fail_silently)
    Feed.drop_table(fail_silently=fail_silently)
    Entry.drop_table(fail_silently=fail_silently)

def get_news(current_date = datetime.date.today()):
    """Grab stored news for specified date."""
    news = []
    try:
        date = Date.get(Date.date == current_date)
    except pdne:
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
    """Update database with new items from the feeds."""
    import feedparser
    from flask import current_app
    today = datetime.date.today()
    try:
        date = Date.get(Date.date == today)
    except pdne:
        date = Date.create(date = today)
    new_items = 0
    for feed in Feed.select():
        link = feed.link
        if not link.startswith('http://'):
            link = 'http://%s' % link
        data = feedparser.parse(link)
        max_items = current_app.config['FEEDLOGGR_MAX_ITEMS'] or 25
        items = min(max_items, len(data.entries))
        with db.database.transaction(): # avoids comitting after each new item
            for i in xrange(items):
                item = data.entries[i]
                try:
                    Entry.create(
                        title = item['title'] or item['link'],
                        link = item['link'],
                        date = date,
                        feed = feed,
                    )
                except pie:
                    pass
                else:
                    new_items += 1
    return new_items

