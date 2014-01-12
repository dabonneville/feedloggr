
import datetime
import unittest

from app import create_app

class FeedloggrTestCase(unittest.TestCase):
    def setUp(self):
        config = {
            'TESTING': True,
            'DATABASE': {
                'name': ':memory:',
                'engine': 'peewee.SqliteDatabase',
            },
        }
        self.app = create_app(config)
        self.client = self.app.test_client()
        from blueprint.utils import create_tables
        create_tables(fail_silently = True)
        self.app.auth.User.create_table(fail_silently = True)

    def tearDown(self):
        from blueprint.utils import drop_tables
        drop_tables(fail_silently = True)
        self.app.auth.User.drop_table(fail_silently = True)

    def populate_db(self):
        from blueprint.models import Dates, Feeds, Entries, db
        today = datetime.date.today()
        date = Dates.create(date = today)
        feed = Feeds.create(title='feed_title', link='feed_link')
        Entries.create(
            title='entry_title', link='entry_link', date=date, feed=feed
        )
        db.database.commit()

    def test_database(self):
        """Test if the database has been created."""
        from blueprint.models import Dates, Feeds, Entries
        self.assertEqual(Dates._meta.db_table, 'dates')
        self.assertEqual(Feeds._meta.db_table, 'feeds')
        self.assertEqual(Entries._meta.db_table, 'entries')

    def test_index_view(self):
        """Test if the view contains items and URLs behave correctly."""
        # TODO/BUG: must pass a test BEFORE we can use client.get()!!!!!
        # Test with an empty database
        tmp = self.client.get('/').data
        self.assertIn('Sorry, no links today!', tmp)
        tmp = self.client.get('/1970-01-01').data
        self.assertIn('Sorry, no links today!', tmp)

        # Test URLs
        tmp = self.client.get('/1970-01-01').data
        self.assertIn('1970-01-02', tmp)
        tmp = self.client.get('/1970-01-0a').status_code
        self.assertEqual(404, tmp)

        # Test with populated database
        self.populate_db()
        tmp = self.client.get('/').data
        self.assertIn('feed_title', tmp)
        self.assertIn('entry_title', tmp)

######################################################################

if __name__ == '__main__':
    unittest.main()
