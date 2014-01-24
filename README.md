Feedloggr
=========
Collect news from your favorite RSS/Atom feeds and show them in your flask application.
This is the bigger brother of [simple_feedlog](https://github.com/lmas/simple_feedlog).

[![Build Status](https://travis-ci.org/lmas/Feedloggr.png?branch=master)](https://travis-ci.org/lmas/Feedloggr)
[![Coverage Status](https://coveralls.io/repos/lmas/Feedloggr/badge.png)](https://coveralls.io/r/lmas/Feedloggr)

Installation
------------
First things first!
You're going to have to download the Feedloggr source to your local box somehow.
The easiest thing at the moment is by cloning this git repo:

    git clone https://github.com/lmas/Feedloggr.git

In order to run Feedloggr, it needs some libraries installed:

    pip install -r requirements.txt

You can now run Feedloggr in your flask app!

Configuration
-------------
Feedloggr has only a few, simple configuration variables it will try to use:

    FEEDLOGGR_MAX_ITEMS = [int]
    Tell Feedloggr how many items it should try to load from a feed when
    updating news.

    FEEDLOGGR_URL = [string]
    Register Feedloggr at this url prefix (example: /feedloggr).

Management
----------
You can easily manage Feedloggr from the builtin web admin interface, from
flask-peewee, by visiting `http://your.domain.com/feedloggr/admin/` and logging
in there.

Before that, you have to setup a admin user. This is easily done with the script
`tools/setup_admin.sh`.

Updating Feedloggr with more, up to date news is done by calling
`feedloggr.utils.update_feeds()` within a [flask app context](http://flask.pocoo.org/docs/appcontext/).
`tools/update.sh` can do this for you easily.

Example
-------
Inside of `example/` is a fully working example app. You can either run `python
app.py`, quick 'n easy, or `python manager.py', with some more functionality.
`manager.py` is using flask-script, which enables some custom commands you can
run from the terminal:

    routes              List all routes for this app.
    feeds               Show a list of all stored feeds.
    shell               Runs a Python shell inside Flask application context.
    update              Update all feeds stored in the database.
    runserver           Runs the Flask development server i.e. app.run()

Run `manager.py -h [command]` for more details.

Contribution
------------
Any and all contributions are welcome! Only requirement is that you make sure to
(at least loosely) follow [PEP8](http://www.python.org/dev/peps/pep-0008/) when
editing the code. Also make sure your code will pass the tests.

The Makefile has some simple utils for helping with the developement, I recommend
you check it out.

Credits
-------
See AUTHORS for a complete list.

License
-------
MIT License, see LICENSE.
