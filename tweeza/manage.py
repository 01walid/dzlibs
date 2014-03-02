# -*- coding: utf-8 -*-
""" Docstrings. """

from flask.ext.script import Manager, Server, prompt_bool
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


@manager.command
def setup():

    from items.models import Category, License

    assets = Category()
    assets.name_fr = 'Resources'
    assets.name_ar = u'مصادر'
    assets.name_en = 'Assets'
    assets.save()

    libraries = Category()
    libraries.name_fr = 'Librairies'
    libraries.name_ar = u'مكتبات برمجية'
    libraries.name_en = 'libraries'
    libraries.save()

    data = Category()
    data.name_fr = u'Données'
    data.name_ar = u'بيانات'
    data.name_en = u'Data'
    data.save()

    templates = Category()
    templates.name_fr = 'Templates'
    templates.name_ar = u'قوالب'
    templates.name_en = 'Templates'
    templates.save()

    # create licenses
    CC0 = License()
    CC0.name = 'Public Domain'
    CC0.link = 'http://creativecommons.org/about/cc0'
    CC0.save()

    CC = License()
    CC.name = 'Creative Commons BY'
    CC.link = 'http://creativecommons.org/licenses/by/4.0/deed.en_US'
    CC.save()

    CC2 = License()
    CC2.name = 'Creative Commons BY SA'
    CC2.link = 'http://creativecommons.org/licenses/by-sa/4.0/deed.en_US'
    CC2.save()

    MIT = License()
    MIT.name = 'MIT'
    MIT.link = 'http://opensource.org/licenses/MIT'
    MIT.save()

    BSD = License()
    BSD.name = 'BSD'
    BSD.link = 'http://opensource.org/licenses/BSD-3-Clause'
    BSD.save()

    WAQF = License()
    WAQF.name = 'WAQF'
    WAQF.link = 'http://ojuba.org/wiki/waqf/license'
    WAQF.save()

    Mozilla = License()
    Mozilla.name = 'Mozilla Public License (MPL)'
    Mozilla.link = 'http://www.mozilla.org/MPL/2.0/'
    Mozilla.save()

    Apache = License()
    Apache.name = 'Apache'
    Apache.link = 'http://www.apache.org/licenses/LICENSE-2.0'
    Apache.save()

    GPL = License()
    GPL.name = 'GPL'
    GPL.link = 'https://www.gnu.org/copyleft/gpl.html'
    GPL.save()

    LGPL = License()
    LGPL.name = 'LGPL'
    LGPL.link = 'http://www.gnu.org/licenses/lgpl-3.0-standalone.html'
    LGPL.save()

    AGPL = License()
    AGPL.name = 'AGPL'
    AGPL.link = 'http://www.gnu.org/licenses/agpl-3.0-standalone.html'
    AGPL.save()


@manager.command
def drop_database():
    """
    DANGEROUS: DROP THE DATABASE.

    It assumes the db name is 'dzlibs', change it otherwise
    """
    from mongoengine import connect

    if prompt_bool("Are you sure you want to lose all your data"):
        db = connect('dzlibs')
        db.drop_database('dzlibs')

if __name__ == '__main__':
    manager.run()
