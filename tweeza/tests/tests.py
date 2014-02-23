# this is a basic test file for now...

from flask.ext.testing import TestCase, Twill


class TestViews(TestCase):

    def create_app(self):
        from app import create_app as app
        self.twill = Twill(app)
        return app

    def setUp(self):
        from manage import setup
        setup()

    def tearDown(self):
        from manage import drop_database
        drop_database()
