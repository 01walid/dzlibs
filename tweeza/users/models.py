# -*- coding: utf-8 -*-

import datetime
from extensions import db, bcrypt


class User(db.Document):

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)

    user_id = db.SequenceField(unique=True)

    is_admin = db.BooleanField(default=False)

    email = db.EmailField(unique=True)

    name = db.StringField(max_length=50)

    lang = db.StringField(max_length=3)
    bio = db.StringField()
    location = db.StringField()
    # Available for hire or not
    hireable = db.BooleanField(default=False)

    github_username = db.StringField(max_length=50)
    github_id = db.IntField()

    twitter_username = db.StringField(max_length=50)
    facebook_username = db.StringField(max_length=100)
    website = db.StringField(max_length=50)

    oauth_token = db.StringField()
    oauth_secret = db.StringField()

    _password = db.StringField()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password,
                                          password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # helpers
    def getGithub(self):
        if self.github_username:
            return "https://github.com/%s" % (self.github_username)
        return ''

    def getTwitter(self):
        if self.twitter_username:
            return "https://twitter.com/%s" % (self.twitter_username)
        return ''

    def getFacebook(self):
        if self.facebook_username:
            return "https://facebook.com/%s" % (self.facebook_username)
        return ''

    # Required for administrative interface
    def __unicode__(self):
        return self.name

    meta = {
        'ordering': ['-created_at']
    }
