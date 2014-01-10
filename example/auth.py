
from flask_peewee.auth import Auth

def init_auth(app, db):
    auth = Auth(app, db)
    return auth
