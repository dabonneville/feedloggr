
import datetime
import unittest

from flask import Flask
from flask_peewee.db import Database

from feedloggr import Feedloggr
from feedloggr.utils import drop_tables, create_tables, update_feeds
from feedloggr.models import feedloggr_Dates, feedloggr_Feeds, feedloggr_Entries

class FeedloggrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            DEBUG=True,
            TESTING=True,
            DATABASE={
                'name': 'test.db',
                'engine': 'peewee.SqliteDatabase',
            },
        )
        self.app.db = Database(self.app)

        tmp = Feedloggr(self.app, self.app.db)
        drop_tables(fail_silently = True)
        create_tables(fail_silently = False)

        self.url = tmp.blueprint.url_prefix
        self.client = self.app.test_client()

    def populate_db(self):
        """Populate the database with some test data."""
        today = datetime.date.today()
        date = feedloggr_Dates.create(date = today)
        feed = feedloggr_Feeds.create(title='feed_title', link='feed_link')
        feedloggr_Entries.create(
            title='entry_title', link='entry_link', date=date, feed=feed
        )

    def test_database_was_populated(self):
        """Test if the database has been created."""
        self.populate_db()
        self.assertEqual(feedloggr_Entries.select().count(), 1)
        tmp = feedloggr_Entries.get(feedloggr_Entries.id == 1)
        self.assertIsInstance(tmp, feedloggr_Entries)

    def test_update_database(self):
        """ Test if we can update the database with new items."""
        self.populate_db()
        with self.app.app_context():
            update_feeds()
        tmp = feedloggr_Entries.select().count()
        self.assertEqual(tmp, 1)

    def test_index_view(self):
        """Test if the view contains items and URLs behave correctly."""
        # Test with an empty database
        tmp = self.client.get(self.url, follow_redirects=True).data
        self.assertIn('Sorry, no links today!', tmp)
        tmp = self.client.get('%s/1970-01-01' % self.url).data
        self.assertIn('Sorry, no links today!', tmp)

        # Test URLs
        tmp = self.client.get('%s/1970-01-01' % self.url).data
        self.assertIn('1970-01-02', tmp)
        tmp = self.client.get('%s/1970-01-0a' % self.url).status_code
        self.assertEqual(404, tmp)

        # Test with populated database
        self.populate_db()
        tmp = self.client.get(self.url, follow_redirects=True).data
        self.assertIn('feed_title', tmp)
        self.assertIn('entry_title', tmp)

######################################################################

def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(
        FeedloggrTestCase
    )
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run()
