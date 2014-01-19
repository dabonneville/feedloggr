
"""Collect news from your favorite RSS/Atom feeds and show them
in your flask application."""

from .views import blueprint
from .models import Dates, Feeds, FeedsAdmin, Entries

def register_admin():
    try:
        from ..main import admin
    except ImportError:
        return False
    else:
        admin.register(Feeds, FeedsAdmin)
        return True
