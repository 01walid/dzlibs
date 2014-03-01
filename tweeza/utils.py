# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import string
import random
import os

from datetime import datetime

ALLOWED_THUMBNAILS = set(['png', 'jpg', 'jpeg', 'gif'])

DISALLOWED_EXTENSIONS = set(['exe'])  # only exe for now to prevent viruses

# Form validation

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16


def get_current_time():
    return datetime.utcnow()


def current_year():
    from datetime import date
    return date.today().year


def allowed_thumbnails(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_THUMBNAILS


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return filename.split('.')[-1].lower() not in DISALLOWED_EXTENSIONS


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e
