# -*- coding: utf-8 -*-
""" Docstrings. """

from flask.ext.script import Manager, Server
from app import create_app


app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server())


@manager.command
def babel_init():
    """ Extract strings to the messages.pot file for translations. """
    import os
    os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .')


@manager.command
def babel_create():
    """
    Create .mo files for Arabic, English and French.

    from the messages.pot file.

    """
    import os
    os.system('pybabel init -i messages.pot -d translations -l fr')
    os.system('pybabel init -i messages.pot -d translations -l ar')
    os.system('pybabel init -i messages.pot -d translations -l en')


@manager.command
def babel_update():
    """ update translations on the 'messages.pot' file. """
    import os
    os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .')
    os.system('pybabel update -i messages.pot -d translations')


@manager.command
def babel_compile():
    """ compile translations to .mo ."""
    import os
    os.system('pybabel compile -d translations')


@manager.command
def clean():
    """
    clean Python '.pyc's files.

    this requires the 'find' command to be installed in case of Windows.

    """
    import os
    os.system("find . -type f -name \"*.pyc\" -delete;")


@manager.command
def delete_users():
    """
    delete all users from database

    """
    from users.models import User
    User.objects().delete()

if __name__ == '__main__':
    manager.run()
