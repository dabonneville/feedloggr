
Feedloggr
=========
Genrate news from RSS/Atom feeds for your flask applications.
This is the bigger brother of simple_feedlog (https://github.com/lmas/simple_feedlog).

Installation
------------
First things first, install the libraries:
    pip install -r requirements.txt

Copy the Feedloggr blueprint into your flask app directory:
    cp -r feedloggr/ /path/to/flask/app

Import and register blueprint in your app:
    from feedloggr import blueprint
    app.register_blueprint(blueprint, url_prefix='/feedloggr')

Make sure you have a peewee database up and running, so Feedloggr can store it's
data somewhere. Feedloggr tries to import the database with a:
    from app import db
You might want to change that in 'feedloggr/models.py' or change your app accordingly.

Register Feedloggr with a management script running flask-script:
    from feedloggr.utils import manager as feedloggr_manager
    manager.add_command('feedloggr', feedloggr_manager)
You can now manage Feedloggr via the command line.

Configuration
-------------
There's only one setting you need to add to your app config:
    FEEDLOGGR_MAX_ITEMS = 50
This tells Feedloggr how many items it should try to insert into the database
each time it's updating it's feeds.
Restart your app and you should now be running Feedloggr! You can now visit it
at 'http://your.flask.site/feedloggr'.

Usage
-----
The only way to manage Feedloggr is for now via flask-script.
Aviable commands are:
    list - Show a list of all stored feeds.
    add <link> [-t title] - Add a new feed with a URL and optionally a title.
    remove <idno> - Remove a feed, using it's ID number.
    update - Update all feeds stored in the database.
You should run the update command daily, so Feedloggr can download new items
and show them for you. This is best done with 'cron' on a Linux host. See 'man cron'.

Example
-------
Inside the directory 'example/' is a simple app which shows you how you can run
Feedloggr.

Credits
-------
See AUTHORS for a complete list.

License
-------
MIT License, see LICENSE.
