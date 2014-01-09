
from flask_peewee.auth import Auth

def setup_auth(app, db):
    auth = Auth(app, db)
    return auth
