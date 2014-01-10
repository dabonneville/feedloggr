
from flask_peewee.auth import Auth

def init_auth(app, db):
    """Setup the auth app."""
    auth = Auth(app, db)
    return auth
