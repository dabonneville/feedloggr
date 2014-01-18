#!/usr/bin/env python2

from flask.ext.script import Manager

from feedloggr.main import app, auth

manager = Manager(app)

@manager.command
def setup():
    """Create tables and admin user."""
    from getpass import getpass
    from peewee import IntegrityError as pie
    from peewee import OperationalError as poe
    from feedloggr.blueprint.utils import create_tables

    print('Creating tables.')
    try:
        create_tables(fail_silently = False)
        auth.User.create_table(fail_silently = False)
    except poe as error:
        print('Error while creating tables: %s' % error)
        return

    print('Creating admin user.')
    admin_name = raw_input('Username: ')
    admin_password = getpass()
    try:
        admin_user = auth.User.create(
            username = admin_name,
            admin=True,
            active=True,
            password = '',
            email='',
        )
        admin_user.set_password(admin_password)
        admin_user.save()
    except pie as error:
        print('Error while creating admin user: %s' % error)
        return
    print('Database was successfully created.')

@manager.command
def drop():
    """Drop all database tables used by feedloggr."""
    from feedloggr.blueprint.utils import drop_tables
    drop_tables()
    auth.User.drop_table(fail_silently=True)
    print('All tables dropped.')

@manager.command
def routes():
    """List all routes for this app."""
    print(app.url_map)

@manager.command
def feeds():
    """Show a list of all stored feeds."""
    from feedloggr.blueprint.models import Feeds
    for feed in Feeds.select():
        print('#%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def add(link, title=''):
    """Add a new feed with a URL and optionally a title."""
    from peewee import IntegrityError as pie
    from feedloggr.blueprint.models import Feeds
    try:
        Feeds.create(title=title or link, link=link)
    except pie as error:
        print('Error while adding new feed: %s' % error)
    else:
        print('New feed has been stored.')

@manager.command
def remove(idno):
    """Remove a feed, using it's ID number."""
    from feedloggr.blueprint.models import Feeds
    try:
        feed = Feeds.get(Feeds.id == idno)
        feed.delete_instance()
    except Exception as error:
        print('Error while removing feed: %s' % error)
    else:
        print('Removed feed #%i %s (%s)' % (feed.id, feed.title, feed.link))

@manager.command
def update():
    """Update all feeds stored in the database."""
    from feedloggr.blueprint.utils import update_feeds
    new_items = update_feeds()
    print('Database was updated with %i new items.' % new_items)

######################################################################

if __name__ == '__main__':
    manager.run()

