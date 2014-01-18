
from flask_peewee.admin import Admin, AdminPanel

from app import app
from auth import auth

from blueprint.models import Feeds, FeedsAdmin, Dates, Entries

class StatsPanel(AdminPanel):
    """Show some simple statistics on the admin dashboard."""
    template_name = 'admin/stats.html'

    def get_context(self):
        feeds = Feeds.select().count()
        dates = Dates.select().count()
        entries = Entries.select().count()
        average_per_day = (float(entries) / (dates or 1))
        average_per_feed = (float(entries) / (feeds or 1))
        return {
            'total_entries': entries,
            'total_days': dates,
            'average_per_day': average_per_day,
            'average_per_feed': average_per_feed,
        }

admin = Admin(app, auth)
admin.register(Feeds, FeedsAdmin)
admin.register_panel('Statistics', StatsPanel)
