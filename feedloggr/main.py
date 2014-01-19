#!/usr/bin/env python2

from app import app, db

from auth import auth
from admin import admin

import blueprint
app.register_blueprint(blueprint.blueprint)
blueprint.register_admin()

admin.setup()

