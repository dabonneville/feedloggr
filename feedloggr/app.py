from flask import Flask
from flask_peewee.db import Database

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

