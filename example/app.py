
from flask import Flask
from peewee import IntegrityError as PIE
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin

from feedloggr import Feedloggr
from feedloggr.models import feedloggr_Feeds, feedloggr_FeedsAdmin

def create_app():
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        SECRET_KEY='supersecret',
        DATABASE={
            'name': 'example.db',
            'engine': 'peewee.SqliteDatabase',
        },
    )
    app.db = Database(app)
    Feedloggr(app, app.db)

    # OPTIONALLY SETUP BEGINS
    # Simple authentication for the admin interface
    app.auth = Auth(app, app.db)
    app.auth.User.create_table(fail_silently=True)
    # Try to create a new admin user, but fail silently if it already exists
    try:
        user = app.auth.User.create(
            username='admin',
            email='.',
            password='',
            admin=True,
            active=True,
       )
    except PIE:
        pass
    else:
        user.set_password('admin')
        user.save()
    # Initialize the admin interface
    app.admin = Admin(app, app.auth)
    app.auth.register_admin(app.admin)
    # Register the feedloggr feeds model
    app.admin.register(feedloggr_Feeds, feedloggr_FeedsAdmin)
    app.admin.setup()
    # OPTIONALLY SETUP ENDS

    return app

###############################################################################

if __name__ == '__main__':
    app = create_app()
    app.run()

