
import datetime
import unittest

from example.app import create_app

from feedloggr import Feedloggr
from feedloggr.utils import drop_tables, create_tables, update_feeds
from feedloggr.models import Dates, Feeds, Entries

class FeedloggrTestCase(unittest.TestCase):
    def setUp(self):
        self.config = {
            'DEBUG': False,
            'TESTING': True,
            'DATABASE': {
                'name': 'test.db',
                'engine': 'peewee.SqliteDatabase',
            },
            'FEEDLOGGR_URL': '/test',
        }
        self.app = create_app(self.config)
        Feedloggr(self.app, self.app.db, self.app.admin)
        self.app.admin.setup()
        self.client = self.app.test_client()

        drop_tables(fail_silently = True)
        create_tables(fail_silently = False)

    def populate_db(self):
        """Populate the database with some test data."""
        today = datetime.date.today()
        date = Dates.create(date = today)
        feed = Feeds.create(title='feed_title', link='feed_link')
        Entries.create(
            title='entry_title', link='entry_link', date=date, feed=feed
        )

    def test_database(self):
        """Test if the database has been created."""
        self.assertEqual(Dates._meta.db_table, 'dates')
        self.assertEqual(Feeds._meta.db_table, 'feeds')
        self.assertEqual(Entries._meta.db_table, 'entries')

    def test_update_database(self):
        """ Test if we can update the database with new items."""
        self.populate_db()
        update_feeds()
        tmp = Entries.select().count()
        self.assertEqual(tmp, 1)

    def test_index_view(self):
        """Test if the view contains items and URLs behave correctly."""
        # Test with an empty database
        tmp = self.client.get('/test/').data
        self.assertIn('Sorry, no links today!', tmp)
        tmp = self.client.get('/test/1970-01-01').data
        self.assertIn('Sorry, no links today!', tmp)

        # Test URLs
        tmp = self.client.get('/test/1970-01-01').data
        self.assertIn('1970-01-02', tmp)
        tmp = self.client.get('/test/1970-01-0a').status_code
        self.assertEqual(404, tmp)

        # Test with populated database
        self.populate_db()
        tmp = self.client.get('/test/').data
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
