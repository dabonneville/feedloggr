#!/usr/bin/env python2

from flask_script import Manager

from app import create_app
from feedloggr import Feedloggr

app = create_app()
Feedloggr(app, app.db, app.admin)
app.admin.setup()
manager = Manager(app)

@manager.command
def routes():
    """List all routes for this app."""
    print(app.url_map)

@manager.command
def feeds():
    """Show a list of all stored feeds."""
    from feedloggr.models import Feeds
    for feed in Feeds.select():
        print('#%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def update():
    """Update all feeds stored in the database."""
    from feedloggr.utils import update_feeds
    new_items = update_feeds()
    print('Database was updated with %i new items.' % new_items)

manager.run()

