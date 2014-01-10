
from flask.ext.script import Manager

from app import app

from feedloggr.models import Date, Feed, Entry

manager = Manager(app)

@manager.command
def setup():
    """Initiate databases."""
    from app import setup_db
    setup_db()

@manager.command
def drop_tables():
    """Drop all database tables used by feedloggr."""
    from feedloggr.utils import drop_tables
    drop_tables()
    app.auth.User.drop_table(fail_silently=True)
    print('All tables dropped.')

@manager.command
def routes():
    """List all routes for this app."""
    print(app.url_map)

@manager.command
def feeds():
    """Show a list of all stored feeds."""
    for feed in Feed.select():#.order_by(Feed.title.desc()):
        print('#%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def add(link, title=''):
    """Add a new feed with a URL and optionally a title."""
    from peewee import IntegrityError as pie
    try:
        Feed.create(title=title or link, link=link)
    except pie as error:
        print('Error while adding new feed: %s' % error)
    else:
        print('New feed has been stored.')

@manager.command
def remove(idno):
    """Remove a feed, using it's ID number."""
    try:
        feed = Feed.get(Feed.id == idno)
        feed.delete_instance()
    except Exception as error:
        print('Error while removing feed: %s' % error)
    else:
        print('Removed feed #%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def update():
    """Update all feeds stored in the database."""
    from feedloggr.utils import update_feeds
    new_items = update_feeds()
    print('Database was updated with %i new items.' % new_items)

