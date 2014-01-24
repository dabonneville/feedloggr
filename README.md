Feedloggr
=========
Collect news from your favorite RSS/Atom feeds and show them in your flask application.
This is the bigger brother of [simple_feedlog](https://github.com/lmas/simple_feedlog).

[![Build Status](https://travis-ci.org/lmas/Feedloggr.png?branch=master)](https://travis-ci.org/lmas/Feedloggr)
[![Coverage Status](https://coveralls.io/repos/lmas/Feedloggr/badge.png)](https://coveralls.io/r/lmas/Feedloggr)

Installation
------------
First things first, clone this git repo to your desired box:

    git clone https://github.com/lmas/Feedloggr.git

You now have a local copy of Feedloggr! But in order to run it, it needs some
libraries installed:

    pip install -r requirements.txt

Next, you need to initiate the database:

    ./manager.py setup

Enter a new name and password for an admin user, so you can log in to the web
interface.
You can now run a local instance, for example by using `manager.py`:

    ./manager.py runserver

Configuration
-------------
A default config is loaded from `feedloggr/config.py`. You can override it's
settings by pointing the `FEEDLOGGR_CONFIG` environment variable to another
config file. Feedloggr will try to load that file from an `instance` dir, which
is not under version control.
See `./tools/run_tests.py` for an example.

Valid config values are, including [Flask's builtins](http://flask.pocoo.org/docs/config/#builtin-configuration-values):

    FEEDLOGGR_MAX_ITEMS = [int]
    Tell Feedloggr how many items it should try to load from a feed when
    updating news.

    FEEDLOGGR_URL = [string]
    Register the Feedloggr blueprint at this url prefix (ie. at "/feedloggr").

Management
----------
You can easily manage Feedloggr from either a web admin interface (go to
`http://localhost:5000/admin/` to login) or from the command line (`manager.py`).
The web interface should be pretty self explanatory, once you login.
`manager.py`, on the other hand, has a range of commands:

    shell               Runs a Python shell inside Flask application context.
    setup               Create tables and admin user.
    drop                Drop all database tables used by feedloggr.
    update              Update all feeds stored in the database.
    remove              Remove a feed, using it's ID number.
    runserver           Runs the Flask development server i.e. app.run()
    add                 Add a new feed with a URL and optionally a title.
    routes              List all routes for this app.
    feeds               Show a list of all stored feeds.

Run `./manager.py -h [command]` for more details.

You should run the update command daily, so Feedloggr can download new items
and show them for you. On a linux host, this is easily done with `cron`.

Contribution
------------
Any and all contributions are welcome! Only requirement is that you make sure to
(at least loosely) follow [PEP8](http://www.python.org/dev/peps/pep-0008/) when
editing the code. Also make sure your code will pass the tests.

Credits
-------
See AUTHORS for a complete list.

License
-------
MIT License, see LICENSE.
