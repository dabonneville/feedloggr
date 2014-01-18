#!/usr/bin/env python2

from app import app, db

from auth import auth
from admin import admin

from blueprint import feedloggr
app.register_blueprint(feedloggr)

admin.setup()

