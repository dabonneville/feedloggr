"""Config for running tests."""

DEBUG = False
TESTING = True
DATABASE = {
    'name': 'test.db',
    'engine': 'peewee.SqliteDatabase',
}

