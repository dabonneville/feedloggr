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
    ADMINUSER = 'admin',
    ADMINPASSWORD = 'admin',
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
    from feedloggr.utils import create_tables
    create_tables()

    from peewee import IntegrityError as pie
    auth.User.create_table(fail_silently=True)
    try:
        admin = auth.User.create(
            username=app.config['ADMINUSER'],
            admin=True,
            active=True,
            password = '',
            email='',
        )
        admin.set_password(app.config['ADMINPASSWORD'])
        admin.save()
    except pie as e:
        pass

