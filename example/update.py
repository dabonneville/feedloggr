
# This is an example of how to update the database with new items.

from feedloggr.utils import update_feeds

def update():
    new_items = update_feeds()
    print('Database was updated with %i new items.' % new_items)

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    update()
