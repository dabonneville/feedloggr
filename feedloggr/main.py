#!/usr/bin/env python2

from app import app, db

from auth import auth
from admin import admin

import blueprint
app.register_blueprint(blueprint.blueprint)

auth.register_admin(admin)
admin.setup()

