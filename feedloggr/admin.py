
from flask_peewee.admin import Admin, ModelAdmin

from blueprint.models import Feed

class FeedAdmin(ModelAdmin):
    """Show pretty admin interface for feeds."""
    columns = ('title', 'link')

def init_admin(app, auth):
    """Setup the admin app."""
    admin = Admin(app, auth)
    admin.register(Feed, FeedAdmin)
    admin.setup()
    return admin
