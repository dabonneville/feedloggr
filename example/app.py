
from flask import Flask
from werkzeug.datastructures import ImmutableDict
from peewee import IntegrityError as PIE
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin

# Silence all but the most critical errors from peewee
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.CRITICAL)

def create_app(config={}):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        DEBUG = True,
        SECRET_KEY = 'supersecret',
        DATABASE = {
            'name': 'example.db',
            'engine': 'peewee.SqliteDatabase',
        },
    )
    app.config.update(config)
    app.db = Database(app)

    app.auth = Auth(app, app.db)
    app.auth.User.create_table(fail_silently=True)
    try:
       user = app.auth.User.create(
               username = 'admin',
               email='.',
               password = '',
               admin=True,
               active=True,
       )
    except PIE:
       pass
    else:
       user.set_password('admin')
       user.save()
    app.admin = Admin(app, app.auth)
    app.auth.register_admin(app.admin)

    return app

######################################################################

if __name__ == '__main__':
    from feedloggr import Feedloggr
    app = create_app()
    Feedloggr(app, app.db, app.admin)
    app.admin.setup()
    app.run(host='0.0.0.0', port=8000)

