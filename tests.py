
import datetime
import unittest

from feedloggr.main import app, auth

from feedloggr.blueprint.utils import drop_tables, create_tables
from feedloggr.blueprint.models import Dates, Feeds, Entries

class FeedloggrTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        drop_tables(fail_silently = True)
        auth.User.drop_table(fail_silently = True)
        create_tables(fail_silently = False)
        auth.User.create_table(fail_silently = False)

    def populate_db(self):
        """Populate the database with some test data."""
        today = datetime.date.today()
        date = Dates.create(date = today)
        feed = Feeds.create(title='feed_title', link='feed_link')
        Entries.create(
            title='entry_title', link='entry_link', date=date, feed=feed
        )

    def create_user(self):
        """Create a admin user."""
        user = auth.User.create(
            username = 'admin',
            admin = True,
            active = True,
            password = '',
            email = '',
        )
        user.set_password('admin')
        user.save()

    def login(self):
        """Login to the admin interface."""
        self.create_user()
        self.client.post('/accounts/login/', data={
            'username': 'admin',
            'password': 'admin',
        })

    def test_database(self):
        """Test if the database has been created."""
        self.assertEqual(Dates._meta.db_table, 'dates')
        self.assertEqual(Feeds._meta.db_table, 'feeds')
        self.assertEqual(Entries._meta.db_table, 'entries')

    def test_index_view(self):
        """Test if the view contains items and URLs behave correctly."""
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

    def test_admin_view(self):
        self.login()
        tmp = self.client.get('/admin/').data
        self.assertIn('Average entries per day: 0.0', tmp)

        self.populate_db()
        tmp = self.client.get('/admin/').data
        self.assertIn('Average entries per day: 1.0', tmp)

######################################################################

def run():
    if not app.testing:
        # Make them think twice before testing, since the db will be wiped
        print('No test config loaded!')
        return

    suite = unittest.TestLoader().loadTestsFromTestCase(
        FeedloggrTestCase
    )
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run()
