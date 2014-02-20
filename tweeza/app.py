# -*- coding: utf-8 -*-
""" The main application entry. """

import os
from flask import Flask, request, g, render_template
# Bluprints:
from frontend.views import frontend
from dashboard.views import dashboard
from users import users, User
from items.views import items
# from flask.ext.security import Security
from utils import current_year
from extensions import (db, mail, babel, login_manager, bcrypt,
                        gravatar, md)
from flask.ext.babel import lazy_gettext as _
from flask.ext.mongoengine import MongoEngineSessionInterface


# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    frontend,
    dashboard,
    users,
    items,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = "DzLibs"
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    """
    Looks for the 'config.cfg' file under the instance folder
    then load it or fallbacks to example.cfg
    """
    config_file = None
    prod = os.environ.get('PRODUCTION')
    if prod and prod.lower() in ['true', '1', 'yes', 'y']:  # in production?
        config_file = os.path.join(app.instance_path, 'production.cfg')
    else:  # No? use development config with Debug mode On
        config_file = os.path.join(app.instance_path, 'config.cfg')

    if not os.path.isfile(config_file):
        config_file = os.path.join(app.instance_path, 'example.cfg')

    try:
        app.config.from_pyfile(config_file)
    except IOError:
        print("didn't find any configuration files!\nexiting...")
        raise SystemExit

    os.environ['DEBUG'] = "1"  # required to test Oauth with github


def configure_extensions(app):
    # flask-mongoengine
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)
    # flask-mail
    mail.init_app(app)

    # flask-babel
    babel.init_app(app)

    # Bcrypt for hashing passwords
    bcrypt.init_app(app)

    # the Gravatar service
    gravatar.init_app(app)

    # Markdown
    md.init_app(app)

    # Debug Toolbar
    if app.debug:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    @babel.localeselector
    def get_locale():
        """
        Get the current request locale.

        returns String

        """
        if not hasattr(g, 'lang'):
            g.lang = 'fr'
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return g.lang or request.accept_languages.best_match(accept_languages)

    # flask-login
    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.reauth'

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

    login_manager.setup_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):

    @app.template_filter('prettify')
    def prettify(datetime):
        import humanize
        humanize.activate(g.lang)
        return humanize.naturaltime(datetime)

    @app.template_filter('what_title')
    def what_title(titles_list):
        new_list = []
        # first get rid of empty titles
        for title in titles_list:
            if title.title:
                new_list.append(title)
        # in those non-empty titles, find the one who matches the user language
        for title in new_list:
            if title.lang == g.lang:
                return title.title
        # no hope? ok, just choose the first in the list!
        if len(new_list) > 0:
            return new_list[0].title
        return _("No title!")  # no luck, but this shouldn't happen


def configure_logging(app):
    """Configure file(info) and email(error) logging."""
    return
    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log,
                                                             maxBytes=100000,
                                                             backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    #app.logger.info("testing info.")
    #app.logger.warn("testing warn.")
    #app.logger.error("testing error.")

    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['MAIL_USERNAME'],
                               app.config['ADMINS'],
                               'O_ops... %s failed!' % app.config['PROJECT'],
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(mail_handler)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass

    @app.url_defaults
    def add_language_code(endpoint, values):

        if hasattr(g, 'lang') and not g.lang:
            g.lang = 'fr'
            values.setdefault('lang', g.lang)

    @app.url_value_preprocessor
    def pull_lang_code(endpoint, values):
        if values:
            g.lang = values.pop('lang', None)
        if hasattr(g, 'lang') and not g.lang:
            g.lang = 'fr'

    @app.context_processor
    def utility_processor():
        return dict(current_year=current_year)


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500


app = create_app()

if __name__ == "__main__":
    app.run()
