
from peewee import IntegrityError as pie
from flask_peewee.auth import Auth

def setup_auth(app, db):
    auth = Auth(app, db)
    auth.User.create_table(fail_silently=True)
    try:
        admin = auth.User.create(
            username=app.config['ADMINUSER'],
            admin=True,
            active=True,
            password = '',
            email='',
        )
        admin.set_password(app.config['ADMINPASSWORD'])
        admin.save()
    except pie as e:
        pass
    return auth
