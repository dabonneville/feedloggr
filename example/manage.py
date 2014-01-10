#!/usr/bin/env python

from flask.ext.script import Manager

from app import app
manager = Manager(app)

from feedloggr.utils import manager as feedloggr_manager
manager.add_command('feedloggr', feedloggr_manager)

@manager.command
def setup():
    """Initiate databases."""
    from app import setup
    setup()

@manager.command
def routes():
    """List all routes for this app."""
    print(app.url_map)

if __name__ == '__main__':
    manager.run()
