
from flask_peewee.admin import Admin, ModelAdmin

from feedloggr.models import Feed

class FeedAdmin(ModelAdmin):
    columns = ('title', 'link')

def init_admin(app, auth):
    admin = Admin(app, auth)
    admin.register(Feed, FeedAdmin)
    admin.setup()
    return admin
