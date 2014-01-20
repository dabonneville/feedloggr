
"""Collect news from your favorite RSS/Atom feeds and show them
in your flask application."""

from .models import Dates, Feeds, FeedsAdmin, Entries
from .utils import create_tables
from .views import blueprint

def setup_blueprint(app, admin):
    try:
        url = app.config['FEEDLOGGR_URL']
    except KeyError:
        url = None
    app.register_blueprint(blueprint, url_prefix=url)
    create_tables(fail_silently=True)
    admin.register(Feeds, FeedsAdmin)

