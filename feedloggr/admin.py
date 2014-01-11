
from flask_peewee.admin import Admin, AdminPanel

from blueprint.models import Feed, FeedAdmin, Date, Entry

class StatsPanel(AdminPanel):
    """Show some simple statistics on the admin dashboard."""
    template_name = 'admin/stats.html'

    def get_context(self):
        feeds = Feed.select().count()
        dates = Date.select().count()
        entries = Entry.select().count()
        average_per_day = (float(entries) / dates)
        average_per_feed = (float(entries) / feeds)
        return {
            'total_entries': entries,
            'total_days': dates,
            'average_per_day': average_per_day,
            'average_per_feed': average_per_feed,
        }

def init_admin(app, auth):
    """Setup the admin app."""
    admin = Admin(app, auth)
    admin.register(Feed, FeedAdmin)
    admin.register_panel('Statistics', StatsPanel)
    admin.setup()
    return admin
