#!/usr/bin/env python

from flask.ext.script import Manager

from app import app
manager = Manager(app)

from feedloggr.utils import manager as feedloggr_manager
manager.add_command('feedloggr', feedloggr_manager)

if __name__ == '__main__':
    manager.run()
