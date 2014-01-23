
"""Collect news from your favorite RSS/Atom feeds and show them
in your flask application."""

from flask import Blueprint

from .models import db_proxy, Feeds, FeedsAdmin
from .views import index
from .utils import create_tables

class Feedloggr():
    def __init__(self, app, db=None, admin=None):
        self.app = app
        if app is not None:
            self.init_app(app, db, admin)

    def init_app(self, app, db, admin):
        blueprint = Blueprint(
            'feedloggr',
            __name__,
            template_folder='templates',
            static_folder='static',
        )

        blueprint.add_url_rule('/', view_func=index)
        blueprint.add_url_rule(
            '/<int:year>-<int:month>-<int:day>',
            view_func=index,
        )

        db_proxy.initialize(db.database)
        create_tables(fail_silently=True)
        admin.register(Feeds, FeedsAdmin)

        app.register_blueprint(
            blueprint,
            url_prefix = app.config.get('FEEDLOGGR_URL', '/feedloggr'),
        )
