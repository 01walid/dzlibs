# this is a basic test file for now...

from flask.ext.testing import TestCase


class TestViews(TestCase):

    def create_app(self):
        from app import create_app as app
        return app

    def setUp(self):
        from manage import setup
        setup()

    def tearDown(self):
        from manage import drop_database
        drop_database()
