
from flask_peewee.auth import Auth

from app import app, db

auth = Auth(app, db)
