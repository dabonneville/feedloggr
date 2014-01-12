from flask import Flask
from flask_peewee.db import Database

######################################################################

# Silence all but the most critical errors from peewee, no more spamming
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.CRITICAL)

db = None

def create_app(config={}):
    """Create a new app instance of feedloggr.

    Optional arguments:
    config - A dict containing config settings for the app.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)
    app.config.update(config)

    global db
    db = Database(app)

    from blueprint import feedloggr
    app.register_blueprint(feedloggr)

    from auth import init_auth
    app.auth = init_auth(app, db)

    from admin import init_admin
    app.admin = init_admin(app, app.auth)

    return app

######################################################################

def setup_db():
    """Create tables and admin user."""
    from getpass import getpass
    from peewee import IntegrityError as pie
    from peewee import OperationalError as poe
    from blueprint.utils import create_tables

    print('Creating database tables.')
    try:
        create_tables(fail_silently = False)
        app.auth.User.create_table(fail_silently = False)
    except poe as error:
        print('Error while creating tables: %s' % error)
        return

    print('Creating admin user.')
    admin_name = raw_input('Username: ')
    admin_password = getpass()
    try:
        admin_user = app.auth.User.create(
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

