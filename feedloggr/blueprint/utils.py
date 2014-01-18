
import datetime

from peewee import IntegrityError as pie
from peewee import DoesNotExist as pdne

from .models import Dates, Feeds, Entries, db

######################################################################

def create_tables(fail_silently=True):
    """Create database tables used by feedloggr."""
    Dates.create_table(fail_silently=fail_silently)
    Feeds.create_table(fail_silently=fail_silently)
    Entries.create_table(fail_silently=fail_silently)

def drop_tables(fail_silently=True):
    """Drop database tables used by feedloggr."""
    Dates.drop_table(fail_silently=fail_silently)
    Feeds.drop_table(fail_silently=fail_silently)
    Entries.drop_table(fail_silently=fail_silently)

def get_news(current_date = datetime.date.today()):
    """Grab stored news for specified date."""
    news = []
    try:
        date = Dates.get(Dates.date == current_date)
    except pdne:
        return news
    for feed in Feeds.select().order_by(Feeds.title.desc()):
        items = Entries.select().where(
            Entries.feed == feed,
            Entries.date == date
        )
        if items.count() > 0:
            news.append((feed, items))
    return news

def update_feeds():
    """Update database with new items from the feeds."""
    import feedparser
    from ..app import app
    today = datetime.date.today()
    try:
        date = Dates.get(Dates.date == today)
    except pdne:
        date = Dates.create(date = today)
    new_items = 0
    for feed in Feeds.select():
        link = feed.link
        if not link.startswith('http://'):
            link = 'http://%s' % link
        data = feedparser.parse(link)
        max_items = app.config['FEEDLOGGR_MAX_ITEMS']
        items = min(max_items, len(data.entries))
        with db.database.transaction(): # avoids comitting after each new item
            for i in xrange(items):
                item = data.entries[i]
                try:
                    Entries.create(
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

