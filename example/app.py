from flask import Flask
from flask_peewee.db import Database

######################################################################

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'supersecret',
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase',
    },
    FEEDLOGGR_MAX_ITEMS = 50,
)

db = Database(app)

from auth import init_auth
auth = init_auth(app, db)

from admin import init_admin
admin = init_admin(app, auth)

from feedloggr import blueprint
app.register_blueprint(blueprint)#, url_prefix='/news')

def setup():
    """Create tables and admin user."""
    from getpass import getpass
    from peewee import IntegrityError as pie
    from peewee import OperationalError as poe
    from feedloggr.utils import create_tables

    print('Creating database tables.')
    try:
        create_tables(fail_silently = False)
        auth.User.create_table(fail_silently = False)
    except poe as e:
        print('Error while creating tables: %s' % e)
        return

    print('Creating admin user.')
    admin_name = raw_input('Username: ')
    admin_password = getpass()
    try:
        admin = auth.User.create(
            username = admin_name,
            admin=True,
            active=True,
            password = '',
            email='',
        )
        admin.set_password(admin_password)
        admin.save()
    except pie as e:
        print('Error while creating admin user: %s' % e)
        return

