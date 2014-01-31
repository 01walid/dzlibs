# -*- coding: utf-8 -*-
""" Configs. """


class Config(object):

    PROJECT = "dzlibs"

    ADMINS = ['01walid@gmail.com']

    DEBUG = False
    TESTING = False
    # secret key, can be generated with os.urandom(24)
    SECRET_KEY = \
        '\x17\x14<\xd5\xf2v\xf0\xb0\xf32\xa3q\x95\x9a6\x17?\xbd]n/\xad\xe1\x88'

    SECURITY_PASSWORD_SALT = "test"
    SECURITY_EMAIL_SENDER = "01walid@gmail.com"
    MONGODB_SETTINGS = {"DB": "dzlibs"}
    SECURITY_POST_LOGIN_VIEW = "/profile"
    SECURITY_POST_CONFIRM_VIEW = "/profile"
    SECURITY_REGISTRABLE = False
    SECURITY_RECOVERABLE = True

    MAIL_SERVER = "in.mailjet.com"
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    # MAIL_USE_SSL = True

    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ACCEPT_LANGUAGES = ['en', 'ar', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'

    GITHUB_CONSUMER_KEY = 'd259d8f16784ca5636d6'
    GITHUB_CONSUMER_SECRET = '0e24f54a407b63b62f77e79fe17f4953957b6697'

    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    )
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Uploads
    UPLOAD_FOLDER = 'uploads/'


class DevelopmentConfig(Config):
    DEBUG = True
    # TESTING = True


class ProductionConfig(Config):
    DEBUG = False
