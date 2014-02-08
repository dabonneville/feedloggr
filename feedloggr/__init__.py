
"""Collect news from your favorite RSS/Atom feeds and show them
in your flask application."""

from flask import Blueprint

from .models import db_proxy, feedloggr_Feeds, feedloggr_FeedsAdmin
from .views import index
from .utils import create_tables

class Feedloggr(object):
    def __init__(self, app=None, *args, **kwargs):
        if app:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, db, admin):
        self.app = app
        # register extension with app
        self.app.extensions = getattr(app, 'extensions', {})
        self.app.extensions['feedloggr'] = self

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
        admin.register(feedloggr_Feeds, feedloggr_FeedsAdmin)

        app.register_blueprint(
            blueprint,
            url_prefix = app.config.get('FEEDLOGGR_URL', '/feedloggr'),
        )
