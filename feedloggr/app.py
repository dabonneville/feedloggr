from flask import Flask
from flask_peewee.db import Database

# Silence all but the most critical errors from peewee, no more spamming
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.CRITICAL)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('feedloggr.config')
app.config.from_envvar('FEEDLOGGR_CONFIG', silent=True)

db = Database(app)

