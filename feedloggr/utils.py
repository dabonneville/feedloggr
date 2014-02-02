
import datetime

from flask import current_app
from peewee import IntegrityError as pie
from peewee import DoesNotExist as pdne

from .models import feedloggr_Dates, feedloggr_Feeds, feedloggr_Entries

######################################################################

def create_tables(fail_silently=True):
    """Create database tables used by feedloggr."""
    feedloggr_Dates.create_table(fail_silently=fail_silently)
    feedloggr_Feeds.create_table(fail_silently=fail_silently)
    feedloggr_Entries.create_table(fail_silently=fail_silently)

def drop_tables(fail_silently=True):
    """Drop database tables used by feedloggr."""
    feedloggr_Dates.drop_table(fail_silently=fail_silently)
    feedloggr_Feeds.drop_table(fail_silently=fail_silently)
    feedloggr_Entries.drop_table(fail_silently=fail_silently)

def get_news(current_date = datetime.date.today()):
    """Grab stored news for specified date."""
    news = []
    try:
        date = feedloggr_Dates.get(feedloggr_Dates.date == current_date)
    except pdne:
        return news
    for feed in feedloggr_Feeds.select().order_by(feedloggr_Feeds.title):
        items = feedloggr_Entries.select().where(
            feedloggr_Entries.feed == feed,
            feedloggr_Entries.date == date
        )
        if items.count() > 0:
            news.append((feed, items))
    return news

def update_feeds():
    """Update database with new items from the feeds."""
    import feedparser
    today = datetime.date.today()
    try:
        date = feedloggr_Dates.get(feedloggr_Dates.date == today)
    except pdne:
        date = feedloggr_Dates.create(date = today)
    new_items = 0
    for feed in feedloggr_Feeds.select():
        link = feed.link
        if not link.startswith('http://'):
            link = 'http://%s' % link
        data = feedparser.parse(link)
        max_items = current_app.config.get('FEEDLOGGR_MAX_ITEMS', 40)
        items = min(max_items, len(data.entries))
        with feedloggr_Entries._meta.database.transaction():
            # avoids comitting after each new item
            for i in xrange(items):
                item = data.entries[i]
                try:
                    feedloggr_Entries.create(
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

