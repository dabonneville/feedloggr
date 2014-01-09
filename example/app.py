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

from auth import setup_auth
auth = setup_auth(app, db)

from feedloggr import blueprint
app.register_blueprint(blueprint)#, url_prefix='/news')

# make sure all tables exists
from feedloggr.utils import create_tables
create_tables()

from admin import setup_admin
admin = setup_admin(app, auth)
