
from flask_peewee.admin import Admin

from blueprint.models import Feed, FeedAdmin

def init_admin(app, auth):
    """Setup the admin app."""
    admin = Admin(app, auth)
    admin.register(Feed, FeedAdmin)
    admin.setup()
    return admin
