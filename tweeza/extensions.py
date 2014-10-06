# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

from flask_mail import Mail
mail = Mail()

from flask.ext.babel import Babel
babel = Babel(default_locale='en')

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

# for the Gravatar service
from flaskext.gravatar import Gravatar
gravatar = Gravatar(size=35, rating='g', default='mm',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True)

from flask.ext.misaka import Misaka
md = Misaka(fenced_code=True, superscript=True, strikethrough=True,
            hard_wrap=True, autolink=True)

from flask.ext.cache import Cache
cache = Cache()  # cache cache :)


def github_oauth(app):
    from rauth.service import OAuth2Service

    github = OAuth2Service(
        name='github',
        base_url='https://api.github.com/',
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        client_id=app.config['GITHUB_CONSUMER_KEY'],
        client_secret=app.config['GITHUB_CONSUMER_SECRET'],
    )
    return github
