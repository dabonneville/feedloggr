
from flask import Flask

######################################################################

#from flask_peewee.db import Database
#db = Database(None)
# HACK: flask-peewee can't do this, use "raw peewee" for now
from flask_peewee.db import SqliteDatabase
db = SqliteDatabase(None)
# END HACK

def create_app():
    app = Flask(__name__)
    app.config['FEEDLOGGR_MAX_ITEMS'] = 50

    #db.init(app)
    # HACK: yep, flask-peewee would have done this for us by now..
    db.init('example.db')
    from flask import g
    @app.before_request
    def before_request():
        g.db = db
        g.db.connect()
    @app.after_request
    def after_request(response):
        g.db.close()
        return response
    # END HACK

    from feedloggr import blueprint
    app.register_blueprint(blueprint)#, url_prefix='/news')
    return app
