
"""Collect news from your favorite RSS/Atom feeds and show them
in your flask application."""

from .views import blueprint
from .models import Dates, Feeds, FeedsAdmin, Entries
from .utils import create_tables

def register_admin():
    try:
        from ..main import admin
    except ImportError:
        return False
    else:
        admin.register(Feeds, FeedsAdmin)
        return True

def setup_blueprint(app):
    try:
        url = app.config['FEEDLOGGR_URL']
    except KeyError:
        url = None
    app.register_blueprint(blueprint, url_prefix=url)
    create_tables(fail_silently=True)
    register_admin()
